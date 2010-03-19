import urllib

try:
    import json
except ImportError:
    import simplejson as json
    
import thing
import command
from utils import Cache

@thing.facet_classes.register
class TwitterFacet(thing.ThingFacet):
    name = "twitter"
    commands = command.thing.add_child(command.FacetCommandSet(name))
    
    def __init__(self, thing_):
        thing.ThingFacet.__init__(self, thing_)
        self.get_info = Cache(self._get_info, expire_seconds=10*60)
    
    @classmethod
    def does_attach(cls, thing):
        return False
        
    @commands.add(u"forget that {thing} is a twitterer",
                  help=u"unset {thing}'s twitter username",
                  exclusive=True)
    def unset_twitterer(self, thing, context):
        del self.data
        self.thing.detach_persistent(self)
        
    @commands.add(u"{thing} has twitter username {username}",
                  help=u"set {thing}'s twitter username to {username}",
                  exclusive=True)
    def set_twitter_username(self, thing, username, context):
        self.username = username
    
    @property
    def username(self):
        if self.has_data and "username" in self.data:
            return self.data["username"]
        else:
            return self.thing.name
        
    @username.setter
    def username(self, value):
        if value != self.data["username"]:
            self.data["username"] = value
            self.get_info.reset()
        
    def _get_info(self):
        about_url = "http://api.twitter.com/1/statuses/user_timeline/{0}.json"
        about = urllib.urlopen(about_url.format(self.username))
        return json.load(about)["data"]

@command.thing.add(u"{thing} is a twitterer",
                   help=u"link {thing}'s twitter account to their user",
                   exclusive=True)
@command.thing_command
def set_twitterer(thing, context):
    thing.attach_persistent(twitterFacet)

@thing.presenters.register(set(["twitterer"]))
def present(thing, context):
    twitter = thing.facets["twitterer"]
    info = thing.facets["twitterer"].get_info()
    text = u"http://twitter.com/{name}: {current_status}".format(
        name          = info[0]["user"]["screen_name"],
        current_status= info[0]["text"])
    return text