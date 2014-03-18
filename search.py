# search engine

import re

from plugins.applications import ApplicationsPlugin

class SearchEngine:

    def __init__(self):

        self.matches = []

        self.plugin = ApplicationsPlugin()


    def search(self, query):

        del self.matches[:]

        # Preprocessing
        query = query.strip()

        # self.re1 = re.compile('^(%s)$' % query)
        # self.re2 = re.compile('^(%s)' % query)
        # self.re3 = re.compile('\\b(%s)' % query)
        # self.re5 = re.compile('%s' % query)

        # self.re4 = None
        # words = re.findall('\\s+', query)
        # if words is not None and len(words) >= 2:
        #     self.re4 = re.compile('\\b(%s)' % ').+\\b('.join(words))

        # self.search_plugin(self.plugin, query)

        # Search
        #self.results.clear()

        matches = self.plugin.get_matches(query)
        self.add(matches, 9)


    def add(self, matches, score):
        for m in matches:
            #m = Match(i, 'desc', score)
            if not m in self.matches:
                self.matches.append(m)

    def search_plugin(self, plugin, query):

        #  create a couple of regexes and try to help with matching
        #  match with these regular expressions (with descending score):
        #  1) ^query$
        #  2) ^query
        #  3) \bquery
        #  4) split to words and seach \bword1.+\bword2 (if there are 2+ words)
        #  5) query
        #  6) split to characters and search \bq.+\bu.+\be.+\br.+\by
        #  7) split to characters and search \bq.*u.*e.*r.*y
        #
        #  The set of returned regular expressions depends on MatcherFlags.

        # 1) ^query$
        matches = filter(self.re1.search, plugin.get_items())
        self.add(matches, 9)

        # 2) ^query
        matches = filter(self.re2.search, plugin.get_items())
        self.add(matches, 8)

        # 3) \bquery
        matches = filter(self.re3.search, plugin.get_items())
        self.add(matches, 7)

        # 4) split to words and seach \bword1.+\bword2 (if there are 2+ words)
        if self.re4 is not None:
            matches = filter(self.re4.search, plugin.get_items())
            self.add(matches, 6)

        # 5) query
        matches = filter(self.re5.search, plugin.get_items())
        self.add(matches, 5)



        # // FIXME: do something generic here
        # if (!(MatcherFlags.NO_REVERSED in match_flags))
        # {
        #   if (escaped_words.length == 2)
        #   {
        #     var reversed = "\\b(%s)".printf (string.join (").+\\b(",
        #                                                 escaped_words[1],
        #                                                 escaped_words[0],
        #                                                 null));
        #     try
        #     {
        #       re = new Regex (reversed, flags);
        #       results[re] = Match.Score.GOOD - Match.Score.INCREMENT_MINOR;
        #     }
        #     catch (RegexError err)
        #     {
        #     }
        #   }
        #   else
        #   {
        #     // not too nice, but is quite fast to compute
        #     var orred = "\\b((?:%s))".printf (string.joinv (")|(?:", escaped_words));
        #     var any_order = "";
        #     for (int i=0; i<escaped_words.length; i++)
        #     {
        #       bool is_last = i == escaped_words.length - 1;
        #       any_order += orred;
        #       if (!is_last) any_order += ".+";
        #     }
        #     try
        #     {
        #       re = new Regex (any_order, flags);
        #       results[re] = Match.Score.AVERAGE + Match.Score.INCREMENT_MINOR;
        #     }
