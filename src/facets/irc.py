import thing
import command
import ircutils

@thing.facet_classes.register
class IRCChannelFacet(thing.ThingFacet):
    name = "ircchannel"    
    commands = command.thing.create_child_set(name)
    
    @classmethod
    def does_attach(cls, thing):
        return thing.name.startswith("#")
        
    @commands.add("join {thing}", help="join the channel {thing}")
    def join(self, thing, context):
        context.bot.join_with_key(thing.name.encode("utf-8"))
        
    @commands.add("leave {thing}", help="leave the channel {thing}")
    def join(self, thing, context):
        channel = thing.name.encode("utf-8")
        context.reply("Bye!", where=channel)
        context.bot.leave(channel)
        
    @property
    def topic(self):
        return self.data.get("topic", None)
        
    @topic.setter
    def topic(self, value):
        self.data["topic"] = value

@thing.presenters.register(set(["ircchannel"]))
def present(thing, context):
    facet = thing.facets["ircchannel"]
    if facet.topic:
        return "Topic: {topic}".format(topic=facet.topic)
        
#TODO: IRCUser facet, with trusted/admin types and verified hostmasks

@thing.facet_classes.register
class IRCUserFacet(thing.ThingFacet):
    name = "ircuser"
    
    @classmethod
    def does_attach(cls, thing):
        # Attached by the listener
        return False

    @property
    def is_verified(self):
        return self.data.get("verified", False)
        
    @is_verified.setter
    def is_verified(self, value):
        self.data["verified"] = value
        
@command.listen.add("{message}")
def message(message, context):
    user_thing = context.bot.things.get_thing(context.nick, context)
    user_thing.attach_persistent("ircuser")
