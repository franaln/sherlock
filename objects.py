# objects

# Base object class: every item is showable in Menu
class Item(object):
    def __init__(self, title, subtitle=''):
        self.title = title
        self.subtitle = subtitle

# Matchs
class Match(Item):
    def __init__(self, title, subtitle='', actionable=False,
                 arg=None, uid=None, score=0, plugin=None):

        Item.__init__(self, title, subtitle)
        self.title = title
        self.subtitle = subtitle
        self.actionable = actionable
        self.arg = arg
        self.uid = uid
        self.score = score
        self.plugin = plugin

    def __eq__(self, other):
        return (self.title == other.title)

# class MatchCommand(Match):
#     """ when the match is basically
#     the action itself """

#     def __init__(self, title, subtitle):
#         Match.__init__(self, title, subtitle)

#     def get_actions(self):
#         yield Perform()

#     def run(self, ctx=None):
#         raise NotImplementedError

#     def wants_context(self):
#         """ Return ``True`` if you want the actions' execution
#         context passed as ctx= in RunnableLeaf.run
#         """
#         return False


# Action
class Action(Item):
    def __init__(self, title, subtitle=''):
        Item.__init__(self, title, subtitle)

    def execute(self, target=None):
        raise Exception('Not implemented')

# class Perform(Action):
#     """Perform the action in a RunnableLeaf"""
#     rank_adjust = 5
#     def __init__(self, name=None):
#         # TRANS: 'Run' as in Perform a (saved) command
#         if not name: name = _("Run")
#         super(Perform, self).__init__(name=name)
#         def wants_context(self):
#             return True
#     def activate(self, leaf, ctx):
#         if leaf.wants_context():
#             return leaf.run(ctx)
#         else:
#             return leaf.run()
#     def get_description(self):
#         return _("Perform command")
