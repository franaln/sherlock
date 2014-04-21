class Item(object):

    def __init__(self, title, subtitle='', category='text', arg=None):
        self.title = title
        self.subtitle = subtitle
        self.category = category
        self.arg = arg

    @classmethod
    def from_dict(cls, d):
        return cls(d['title'], d['subtitle'], d['category'], d['arg'])

    def to_dict(self):
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'category': self.category,
            'arg': self.arg
        }







    # @classmethod
    # def unicode(cls, value):
    #     try:
    #         items = value.iteritems()
    #     except AttributeError:
    #         return unicode(value)
    #     else:
    #         return dict(map(unicode, item) for item in items)


    # def __str__(self):
    #     return tostring(self.xml(), encoding='utf-8')

    # def xml(self):
    #     item = Element(u'item', self.unicode(self.attributes))
    #     for attribute in (u'title', u'subtitle', u'icon'):
    #         value = getattr(self, attribute)
    #         if value is None:
    #             continue
    #             if len(value) == 2 and isinstance(value[1], dict):
    #                 (value, attributes) = value
    #             else:
    #                 attributes = {}
    #                 SubElement(item, attribute, self.unicode(attributes)).text = unicode(value)
    #             return item
