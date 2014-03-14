from plugin import Plugin
from match import Match
from actions import Run

class Applications(Plugin):
    """ Open apps. Show recent apps first """

    def __init__(self):
        Plugin.__init__('Applications', 'app')

        self.max_recent = 50 # Number of recent commands to track
        # self.recent_cache = "$cachedir/apps_recent"
        # self.rest_cache = "$cachedir/apps_all"

    def get_actions(self):
        return [Run,]

    def get_matches(self, query):

        apps = open('/home/fran/.cache/sherlock/apps_recent').read().split('\n')
        matches = []

        for app in apps:
            if query in app.lower():
                m = Match(app, '')
                matches.append(m)

        return matches

        # os.mkdir -p $cachedir
        #     touch $recent_cache

        #     IFS=:
        #     if stest -dqr -n "$rest_cache" $PATH; then
        #         stest -flx $PATH | sort -u | grep -vf "$recent_cache" > "$rest_cache"
        #     fi

        #     IFS=" "
        #     cmd=$(cat "$recent_cache" "$rest_cache" | xdmenu "apps") || exit

        #     if ! grep -qx "$cmd" "$recent_cache" &> /dev/null; then
        #         grep -vx "$cmd" "$rest_cache" > "$rest_cache.$$"
        #         mv "$rest_cache.$$" "$rest_cache"
        #     fi
        #     echo "$cmd" > "$recent_cache.$$"
        #     grep -vx "$cmd" "$recent_cache" | head -n "$max_recent" >> "$recent_cache.$$"
        #     mv "$recent_cache.$$"  "$recent_cache"

        #     ($cmd | ${SHELL:-"/bin/sh"} &)
        #     ;;
