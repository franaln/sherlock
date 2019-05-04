from gi.repository import GLib, Gtk

class IconCache:

    def __init__(self):

        self._map = {}
        self.theme = Gtk.IconTheme.get_default()

    def clear_cache(self):
        del self._map

    def get_icon(self, name, size):
        if not name:
            return None

        key = "%s" % (name)

        pixbuf = self._map.get(key)

        if pixbuf is None:
            pixbuf = self.get_pixbuf(name, size)
            if pixbuf is None:
                pixbuf = self.get_pixbuf("unknown", size)

            if pixbuf is None:
                return None

            self._map[key] = pixbuf

        return pixbuf


    def get_pixbuf(self, name, size):

        try:
            # icon = GLib.Icon.new_for_string(name)
            # if icon is None:
            #     return None

            # iconinfo = self.theme.lookup_by_gicon(icon, size, Gtk.IconLookupFlags.FORCE_SIZE)
            # if iconinfo is None:
            #     return None

            # icon_pixbuf = iconinfo.load_icon()
            # if icon_pixbuf is not None:
            #     return icon_pixbuf

            # return Gdk.PixBuf
            return self.theme.load_icon(name, size, Gtk.IconLookupFlags.FORCE_SIZE)

        except:
            pass

        return None
