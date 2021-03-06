import thing
import command
from twisted.python import log


created_timestamp = thing.created_timestamp


@thing.facet_classes.register
class DescriptionFacet(thing.ThingFacet):
    name = "description"
    commands = command.thing.add_child(command.FacetCommandSet(name))

    @classmethod
    def does_attach(cls, thing):
        return True

    @commands.add(u"{thing} is {description}",
                  help=u"add a description to {thing}")
    def describe(self, thing, description, context):
        self.descriptions.append({"created": created_timestamp(context),
                                  "text": description})

    @commands.add(u"forget that {thing} is {description}",
                  help=u"drop a {description} for {thing}")
    def forget(self, thing, description, context):
        log.msg(self.descriptions)
        for desc in self.descriptions:
            if desc["text"] == description:
                self.descriptions.remove(desc)
                log.msg("removed %s" % desc)

    @property
    def data(self):
        return self.thing.data.setdefault(self.__class__.name, [])

    @property
    def descriptions(self):
        return self.data

    def present(self):
        return u", ".join(desc["text"] for desc in self.descriptions) \
            or u"<no description>"


@thing.presenters.register(set(["name", "description"]))
def present(thing, context):
    if thing.facets["description"].descriptions:
        text = u"{name}: {descriptions}".format(
            name         = thing.describe(context, facets=set(["name"])),
            descriptions = thing.facets["description"].present())
        return text
    else:
        return thing.describe(context, facets=set(["name"]))
    
@thing.presenters.register(set(["name", "karma", "description"]))
def present(thing, context):
    name_display = thing.describe(context, facets=set(["name", "karma"]))
    if thing.facets["description"].descriptions:
        text = u"{name}: {descriptions}".format(
            name         = name_display,
            descriptions = thing.facets["description"].present())
        return text
    else:
        return name_display
