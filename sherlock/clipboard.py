import os
import json
import logging
from datetime import datetime, timedelta
from gi.repository import Gtk, Gdk, GLib

class Clipboard:

    def __init__(self, path):

        self.logger = logging.getLogger(__name__)

        self.path = path

        self.selection_primary = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        self.selection_clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        self.selection_clipboard.connect('owner-change', self.handle_owner_change_clipboard)
        self.selection_primary.connect('owner-change', self.handle_owner_change_primary)

        try:
            self.load()
        except:
            self.history = []
        self.history_changed = False

        self.last_copied = ''
        self.last_copied_time = None

    def load(self):
        self.logger.info('loading clipboard history from %s' % self.path)
        with open(self.path, 'r') as f:
            self.history = json.loads(f.read())

    def save(self):
        if not self.history_changed:
            return
        self.logger.info('saving clipboard history to %s' % self.path)
        with open(self.path, 'w') as f:
            f.write(json.dumps(self.history))
        return True

    def remove_history(self, text):
        for d in self.history:
            if text == d['text']:
                self.history.remove(d)
                self.history_changed = True
                break

    def handle_owner_change_primary(self, clipboard, event):
        self.update(clipboard, 'PRIMARY')

    def handle_owner_change_clipboard(self, clipboard, event):
        self.update(clipboard, 'CLIPBOARD')

    def update(self, clipboard, selection_type):

        text = clipboard.wait_for_text()

        if text is None:
            return

        if self.last_copied and (text == self.last_copied or (datetime.now() - self.last_copied_time) < timedelta(seconds = 1)):
            return

        self.logger.info('copying %s to the clipboards' % text.split('\n')[0][:50])

        # remove from history if already exists
        self.remove_history(text)

        # Check for growing or shrinking, but ignore duplicates
        try:
            last_item = self.history[0]
        except IndexError:
            last_item = dict()

        if last_item and text != last_item['text'] and (text in last_item['text'] or last_item['text'] in text):
            # Make length difference a positive number before comparing
            if abs(len(text) - len(last_item['text'])) <= 10:
                # new selection is a longer/shorter version of previous
                pass #self.history.pop()

        # Insert selection into history
        timestamp = datetime.now()
        self.last_copied = text
        self.last_copied_time = timestamp

        # create Item
        it = {
            'text': text,
            'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.history.insert(0, it)
        self.history_changed = True

        # Sync both clipboard
        if selection_type == 'CLIPBOARD':
            self.selection_primary.set_text(text, -1)
        elif selection_type == 'PRIMARY':
            self.selection_clipboard.set_text(text, -1)

        return True

    # def copy_image(self, img):
    #     if self.image.get_storage_type() == Gtk.ImageType.PIXBUF:
    #         self.clipboard.set_image(self.image.get_pixbuf())
    #     else:
    #         print("No image has been pasted yet.")

    def extract_url(self, text):
        pattern = r'\b\S+://\S+\b'
        return re.find_all(pattern, text)[0]

    def extract_email(self, text):
        pattern = r'\b\S+\@\S+\.\S+\b'
        return re.find_all(pattern, text)[0]

    def get_history(self):

        items = []
        for data_dict in self.history:

            text = data_dict['text']

            if '\n' in text:
                it_text = '%s...' % text.split('\n')[0][:50]
            elif len(text) > 50:
                it_text = '%s...' % text[:50]
            else:
                it_text = text

            td = (datetime.now() - datetime.strptime(data_dict['timestamp'], '%Y-%m-%d %H:%M:%S'))

            if td.days >= 1:
                it_time = 'Copied at %s' % data_dict['timestamp']
            elif td.seconds < 60:
                it_time = 'Copied %i seconds ago' % td.seconds
            elif td.seconds < 3600:
                it_time = 'Copied %i minutes ago' % (td.seconds/60)
            elif td.seconds < 24*3600:
                it_time = 'Copied %i hours ago' % (td.seconds/3600)

            it = Item(text=it_text, subtext=it_time, arg=text, keys=text, category='cb')

            items.append(it)

        return items

    def get_text(self):
        text = clipboard.wait_for_text()
        if text is None or not text:
            text = ''
        return text

    # def get_text(self):
    #     text = self.clipboard.wait_for_text()
    #     # if text is not None:
    #     #     self.entry.set_text(text)
    #     # else:
    #     #     print("No text on the clipboard.")
    #     return text

    # def paste_image(self, widget):
    #     image = self.clipboard.wait_for_image()
    #     if image is not None:
    #         self.image.set_from_pixbuf(image)

    def __del__(self):
        self.save()
