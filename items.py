# item: base class for menu item

class Item(object):
    def __init__(self, title, subtitle=''):
        self.title = title
        self.subtitle = subtitle

class Match(Item):
    def __init__(self, title, subtitle='', arg=None, valid=False,
                 uid=None, score=0, plugin_name=None):

        Item.__init__(self, title, subtitle)
        self.title = title
        self.subtitle = subtitle
        self.arg = arg
        self.valid = valid
        self.uid = uid
        self.score = score
        self.plugin_name = plugin_name

    def __eq__(self, other):
        return (self.title == other.title)


class Action(Item):
    def __init__(self, title, subtitle):
        Item.__init__(self, title, subtitle)

    def execute(self):
        raise Exception('Not implemented')


class Trigger:
    pass

    # @property
    # def elem(self):
    #     """Create and return feedback item for Alfred.

    #     :returns: :class:`ElementTree.Element <xml.etree.ElementTree.Element>`
    #         instance for this :class:`Item` instance.
    #     """

    #     attr = {}
    #     if self.valid:
    #         attr['valid'] = 'yes'
    #     else:
    #         attr['valid'] = 'no'
    #     # Optional attributes
    #     for name in ('uid', 'type', 'autocomplete'):
    #         value = getattr(self, name, None)
    #         if value:
    #             attr[name] = value

    #     root = ET.Element('item', attr)
    #     ET.SubElement(root, 'title').text = self.title
    #     ET.SubElement(root, 'subtitle').text = self.subtitle
    #     if self.arg:
    #         ET.SubElement(root, 'arg').text = self.arg
    #     # Add icon if there is one
    #     if self.icon:
    #         if self.icontype:
    #             attr = dict(type=self.icontype)
    #         else:
    #             attr = {}
    #         ET.SubElement(root, 'icon', attr).text = self.icon
    #     return root
