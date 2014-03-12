from gi.repository import Gtk, Gdk, GObject, Pango, PangoCairo
from gi.repository.GdkPixbuf import Pixbuf

# class ActionSelector(Gtk.Bin):
#     __gtype_name__ = 'ActionSelector'

#     def __init__(self):
#         super().__init__()

#         self.names = ['All',]

#         self.label = Gtk.Label('')
#         self.label.show()
#         self.add(self.label)
#         self.selected = 0

#         #self.labels = {}
#         #self.init_labels()
#         self.update()

#     def add_name(self, name):
#         self.names.append(name)
#         self.update()

#     def update(self):
#         label = ''
#         for i, name in enumerate(self.names):
#             if i == self.selected:
#                 label += ' <span size=\"medium\"><b>&lt; %s &gt;</b></span> ' % name
#             else:
#                 label += ' <span size=\"small\">%s</span> ' % name

#             self.label.set_markup(label)

#     def select_prev(self):
#         self.selected -= 1
#         self.update()

#     def select_next(self):
#         self.selected += 1
#         self.update()



class SearchBar(Gtk.SearchEntry):
    __gtype_name__ = 'SearchBar'

    def __init__(self):
        super().__init__()
        self.placeholder_text = 'Search...'

        self.query = ''
        self.text = ''

    def update(self):
        self.set_text(self.text)

    def set_text(self, text):
        self.text = text
        self.update()

class CellRendererCustom(Gtk.CellRenderer):
    width = GObject.property(type=int, default=0)
    height = GObject.property(type=int, default=50)

    header = GObject.property(type=str, default='')
    header_font_size = GObject.property(type=int, default=11)
    header_foreground_color = GObject.property(type=str, default="#000000")

    text = GObject.property(type=str, default='')
    text_font_size = GObject.property(type=int, default=8)
    text_foreground_color = GObject.property(type=str, default="#6f6f6f")

    date_timestamp = GObject.property(type=float, default=0)
    date_format = GObject.property(type=str, default="%c")
    date_foreground_color = GObject.property(type=str, default="#6f6f6f")
    date_font_size = GObject.property(type=int, default=8)

    # tags = GObject.property(type=GObject.TYPE_PYOBJECT)
    # tag_background_color = GObject.property(type=str, default="#0678B1")
    # tag_foreground_color = GObject.property(type=str, default="#FFFFFF")
    # tag_font_size = GObject.property(type=int, default=8)

    line_spacing = GObject.property(type=int, default=4)
    margin = GObject.property(type=int, default=10)

    image_path = GObject.property(type=str, default='')
    image_preserve_aspect_ration = GObject.property(type=bool, default=True)
    image_max_width = GObject.property(type=int, default=150)

    def __init__(self):
        super(CellRendererCustom, self).__init__()

    def gdk_to_rgb(self, gdk):
        return max(0.0, min(gdk, 1.0)) * 255.0

    def rgba_to_markup(self, rgba):
        return "#%02x%02x%02x" % (
            self.gdk_to_rgb(rgba.red),
            self.gdk_to_rgb(rgba.green),
            self.gdk_to_rgb(rgba.blue)
        )

    def get_foreground_rgba(self, widget, selected):
        return widget.get_style_context().get_color(
            Gtk.StateFlags.SELECTED if selected else Gtk.StateFlags.NORMAL
        )

    def set_source_from_col(self, ctx, col, alpha):
        """Take a cairo context and set the source to col"""
        ctx.set_source_rgba(col.red, col.green, col.blue, 0.5) #alpha)

    def get_datetime_string(self):
        #date = datetime.datetime.fromtimestamp(self.date_timestamp)
        #string = date.strftime(self.date_format)

        return 'Hola' #string

    # def get_tag_layout(self, widget, tag):
    #     markup = (
    #         "<span background='%s' foreground='%s' "
    #         "font='%s' weight='bold'> %s </span>"
    #     )
    #     markup = markup % (
    #         self.tag_background_color,
    #         self.tag_foreground_color,
    #         self.tag_font_size,
    #         tag
    #     )

    #     font = Pango.FontDescription()
    #     font.set_size(self.tag_font_size * Pango.SCALE)

    #     layout = widget.create_pango_layout('')
    #     layout.set_font_description(font)
    #     layout.set_markup(markup, -1)
    #     layout.set_alignment(Pango.Alignment.RIGHT)
    #     layout.set_ellipsize(Pango.EllipsizeMode.END)

    #     return layout

    def do_set_property(self, pspec, value):
        setattr(self, pspec.name, value)

    def do_get_property(self, pspec):
        return getattr(self, pspec.name)

    def do_get_size(self, widget, cell_area):
        # FIXME: get_size() doc's say it's deprectated,
        # but do_get_preferred_size does not seem to work yet.
        return (0, 0, self.width, self.height)

    def do_render(self, ctx, widget, background_area, cell_area, flags):
        selected = (flags & Gtk.CellRendererState.SELECTED) != 0
        prelit = (flags & Gtk.CellRendererState.PRELIT) != 0

        if self.image_path:
            self.image_size = self.render_image(
                widget,
                cell_area,
                ctx,
                selected
            )
        else:
            self.image_size = {
                "width": 0,
                "height": 0
            }

        self.header_rect = self.render_header(widget, cell_area, ctx, selected)
        #self.date_rect = self.render_date(widget, cell_area, ctx, selected)
        self.text_rect = self.render_text(widget, cell_area, ctx, selected)

        # if selected:
        #     self.tags_rect = self.render_tags(widget, cell_area, ctx, selected)
        # elif prelit:
        #     self.tags_rect = self.render_tags(widget, cell_area, ctx, selected)
        # self.render_prelit(widget, cell_area, ctx, selected)

    def render_header(self, widget, cell_area, ctx, selected):
        if not selected:
            foreground_color = self.header_foreground_color
        else:
            foreground_color = self.rgba_to_markup(
                self.get_foreground_rgba(widget, selected)
            )

        header_markup = "<span foreground='%s'>%s</span>"
        header_markup = header_markup % (
            foreground_color,
            self.header
        )

        font_header = Pango.FontDescription()
        #font_header.set_size(self.header_font_size * Pango.SCALE)

        layout_header = widget.create_pango_layout('')
        layout_header.set_font_description(font_header)
        layout_header.set_markup(header_markup, -1)
        layout_header.set_alignment(Pango.Alignment.LEFT)
        layout_header.set_ellipsize(Pango.EllipsizeMode.END)

        [ink_rect, logical_rect] = layout_header.get_pixel_extents()

        if ctx and cell_area:
            layout_width = (
                cell_area.width
                - self.margin * 2
                - self.image_size["width"]
            )
            layout_width *= Pango.SCALE
            layout_header.set_width(layout_width)

            layout_height = logical_rect.height + self.margin
            layout_height *= Pango.SCALE
            layout_header.set_height(layout_height)

            y = cell_area.y + self.line_spacing
            x = cell_area.x + self.margin

            ctx.move_to(x, y)
            PangoCairo.show_layout(ctx, layout_header)

        return logical_rect

    def render_text(self, widget, cell_area, ctx, selected):
        if not selected:
            foreground_color = self.text_foreground_color
        else:
            foreground_color = self.rgba_to_markup(
                self.get_foreground_rgba(widget, selected)
            )

        text_markup = "<span foreground='%s'>%s</span>"
        text_markup = text_markup % (foreground_color, self.text)

        font_text = Pango.FontDescription()
        font_text.set_size(self.text_font_size * Pango.SCALE)

        layout_text = widget.create_pango_layout('')
        layout_text.set_font_description(font_text)
        layout_text.set_markup(text_markup, -1)
        layout_text.set_alignment(Pango.Alignment.LEFT)
        layout_text.set_ellipsize(Pango.EllipsizeMode.END)

        [ink_rect, logical_rect] = layout_text.get_pixel_extents()

        if ctx and cell_area:
            layout_width = (
                cell_area.width
                - self.margin * 2
                - self.image_size["width"]
            )
            layout_width *= Pango.SCALE
            layout_text.set_width(layout_width)

            layout_height = (
                cell_area.height
                - self.header_rect.height
                #- self.date_rect.height
                #- self.line_spacing * 2
            )
            layout_height *= Pango.SCALE
            layout_text.set_height(layout_height)

            y = (
                cell_area.y
                + self.header_rect.height
                + self.header_rect.y
                #+ self.line_spacing * 2
            )
            x = cell_area.x + self.margin

            ctx.move_to(x, y)
            PangoCairo.show_layout(ctx, layout_text)

        return logical_rect

    def render_date(self, widget, cell_area, ctx, selected):
        if not selected:
            foreground_color = self.date_foreground_color
        else:
            foreground_color = self.rgba_to_markup(
                self.get_foreground_rgba(widget, selected)
            )

        date_string = self.get_datetime_string()
        date_markup = (
            "<span foreground='%s' style='italic' "
            "weight='bold'>%s</span>"
        )
        date_markup = date_markup % (foreground_color, date_string)

        font_date = Pango.FontDescription()
        font_date.set_size(self.date_font_size * Pango.SCALE)

        layout_date = widget.create_pango_layout('')
        layout_date.set_font_description(font_date)
        layout_date.set_markup(date_markup, -1)
        layout_date.set_alignment(Pango.Alignment.LEFT)
        layout_date.set_ellipsize(Pango.EllipsizeMode.END)

        [ink_rect, logical_rect] = layout_date.get_pixel_extents()

        if ctx and cell_area:
            layout_width = logical_rect.width + self.margin
            layout_width *= Pango.SCALE
            layout_date.set_width(layout_width)

            layout_height = logical_rect.height + self.line_spacing
            layout_height *= Pango.SCALE
            layout_date.set_height(layout_height)

            y = cell_area.y + cell_area.height - logical_rect.height - self.line_spacing
            x = logical_rect.x + self.margin

            ctx.move_to(x, y)
            PangoCairo.show_layout(ctx, layout_date)

        return logical_rect

    # def render_tags(self, widget, cell_area, ctx, selected):
    #     return
    #     if ctx and cell_area:
    #         backgrounds_width = 0
    #         backgrounds_height = 0
    #         tags_width = 0
    #         tags_height = 0
    #         tags_margin = self.margin * 0.5

    #         for tag in self.tags:
    #             layout_tag = self.get_tag_layout(widget, tag)

    #             [ink_rect, logical_rect] = layout_tag.get_pixel_extents()

    #             layout_width = logical_rect.width + tags_margin
    #             tags_width += layout_width
    #             layout_tag.set_width(layout_width * Pango.SCALE)

    #             layout_height = logical_rect.height + self.line_spacing
    #             layout_tag.set_height(layout_height * Pango.SCALE)

    #             if layout_height > tags_height:
    #                 tags_height = layout_height

    #             background_width = layout_width
    #             backgrounds_width += background_width

    #             background_height = layout_height + self.line_spacing

    #             if background_height > backgrounds_height:
    #                 backgrounds_height = background_height

    #             background_y = (
    #                 cell_area.y
    #                 + cell_area.height
    #                 - background_height
    #                 - self.date_rect.height
    #                 - self.line_spacing
    #             )
    #             background_x = (
    #                 cell_area.width
    #                 - backgrounds_width
    #                 - tags_margin
    #             )

    #             ctx.set_source_rgba(0, 0, 0, 0.7)
    #             ctx.rectangle(
    #                 background_x,
    #                 background_y,
    #                 background_width,
    #                 background_height
    #             )
    #             ctx.fill()

    #             y = (
    #                 cell_area.y
    #                 + cell_area.height
    #                 - layout_height
    #                 - self.date_rect.height
    #                 - self.line_spacing
    #             )
    #             x = (
    #                 cell_area.width
    #                 - tags_width
    #                 - tags_margin * 1.5
    #             )

    #             border_line_width = 1.5
    #             ctx.rectangle(
    #                 x + tags_margin,
    #                 y,
    #                 layout_width - tags_margin,
    #                 layout_height - self.line_spacing
    #             )
    #             ctx.set_source_rgb(255, 255, 255)
    #             ctx.set_line_width(border_line_width)
    #             ctx.stroke()

    #             ctx.move_to(x, y)
    #             PangoCairo.show_layout(ctx, layout_tag)

    #         # return logical_rect

    def render_image(self, widget, cell_area, ctx, selected):
        opacity = 0.5 if selected else 1.0
        size = {
            "width": 0,
            "heitgh": 0
        }

        if ctx and cell_area:
            if self.image_preserve_aspect_ration:
                width = -1
            else:
                width = min(int(cell_area.width / 3.5), self.image_max_width)

            height = (
                cell_area.height
                - self.line_spacing * 2
            )

            try:
                pixbuf = Pixbuf.new_from_file_at_scale(
                    self.image_path,
                    width,
                    height,
                    self.image_preserve_aspect_ration
                )
            except Exception as e:
                print (e)
                return size

            size["width"] = pixbuf.get_width()
            size["height"] = pixbuf.get_height()

            y = cell_area.y + self.line_spacing
            x = cell_area.width - (size["width"] + self.margin)

            Gdk.cairo_set_source_pixbuf(ctx, pixbuf, x, y)
            ctx.paint_with_alpha(opacity)

        return size

    def render_prelit(self, widget, cell_area, ctx, selected):
        if selected:
            return

        (x, y, width, height) = (
            cell_area.x,
            cell_area.y,
            cell_area.width,
            cell_area.height
        )

        rect_width = 3
        rect_margin = 1
        style = widget.get_style_context()
        color = style.get_border_color(Gtk.StateFlags.SELECTED)

        self.set_source_from_col(ctx, color, 1)

        ctx.rectangle(
            x + rect_margin,
            y + self.line_spacing,
            rect_width,
            height - self.line_spacing * 2
        )
        ctx.fill()

    # def on_motion_notify(self, tree, event):
    #     event_x = int(event.x)
    #     event_y = int(event.y)

    #     try:
    #         path, column, cell_x, cell_y = tree.get_path_at_pos(
    #             event_x,
    #             event_y
    #         )
    #     except TypeError:
    #         return

    #     cell_area = tree.get_cell_area(path, column)

    #     if event_x >= cell_area.x and event_x < cell_area.x + cell_area.width and \
    #        event_y > cell_area.y and  event_y < cell_area.y + cell_area.height:
    #         pass

class ResultsBox(Gtk.Box):
    __gtype_name__ = 'ResultsBox'

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.create_model()
        self.create_view()

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.view)

        self.pack_start(scroll, True, True, 0)

    def clear(self):
        self.model.clear()

    def add_result(self, result):
        self.model.append([result.name, result.description, 0.0])

    def create_model(self):
        # model
        self.model = Gtk.ListStore(str, str, float)
        #self.model.set_sort_func(5, self.compare_fn, None)
        #self.model.set_sort_column_id(5, Gtk.SortType.DESCENDING)

    def create_view(self):

        self.renderer = CellRendererCustom()

        column = Gtk.TreeViewColumn(
            'Text',
            self.renderer,
            header=0,
            text=1,
        )
        #image_path=3,
        #date_timestamp=2)
        column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        column.set_cell_data_func(self.renderer, self.load_data)

        self.view = Gtk.TreeView(model=self.model)
        self.view.set_activate_on_single_click(True)
        self.view.set_headers_visible(False)
        self.view.set_enable_search(False)

        #self.tree_view.append_column(column)
        self.view.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)
        self.view.set_can_focus(False)
        self.view.set_fixed_height_mode(True)
        #self.view.connect(
        #    "motion-notify-event",
        #    self.renderer.on_motion_notify
        #)

        self.selection = self.view.get_selection()


        # # Column title/tags
        # cell_title = TwoCellRenderer() #Gtk.CellRendererText()
        # cell_title.props.wrap_mode = Pango.WrapMode.WORD
        # cell_title.props.wrap_width = 300

        # cell_tags = Gtk.CellRendererText()
        # cell_tags.props.foreground = 'grey'
        # cell_tags.props.style = Pango.Style.ITALIC
        # cell_tags.props.scale = 0.8

        # column_note = Gtk.TreeViewColumn('Note', cell_title)
        # column_note.set_min_width(100)
        # column_note.set_expand(True)

        # column_note.set_cell_data_func(cell_title, self.cell_data_fn_title)
        # column_note.set_cell_data_func(cell_tags, self.cell_data_fn_tags)

        # column_note.pack_end(cell_tags, False)

        # # mtime column
        # cell_utime = Gtk.CellRendererText()
        # cell_utime.props.foreground = 'grey'

        # column_utime = Gtk.TreeViewColumn('Updated', cell_utime)
        # column_utime.set_min_width(50)
        # column_utime.set_cell_data_func(cell_utime, self.cell_data_fn_utime)

        self.view.append_column(column)

    def load_data(self, column, cell, model, iter, data):
        pass
        # row_index = model.get_path(iter)[0]
        # max_index = len(model)

        # if row_index >= (max_index - self.min_left):
        #     self.load_rows(max_index - 1, self.max_rows_number)

    def load_rows(self, last_index, rows):
        pass
        # if last_index >= self.total_rows:
        #     return

        # number = last_index + 1

        # if(rows > self.total_rows):
        #     rows = self.total_rows

        # images = ['', '', '']

        # if self._img_dir:
        #     images.extend(glob.glob(self._img_dir + "/*.jpg"))

        # for row in range(rows):
        #     title = self.random_title(20)
        #     title = '%s. %s' % (number, title)
        #     number += 1

        #     words = self.lorem_ipsum.split(" ")
        #     random.shuffle(words)
        #     lorem_ipsum = ' '.join(words)

        #     item = [
        #         title,
        #         lorem_ipsum[0: random.randint(0, len(lorem_ipsum))],
        #         random.choice(images),
        #         self.random_timestamp(),
        #         self.random_tags(0, 10)
        #     ]
        #     self.store.append(item)


    # def cell_data_fn_title(self, column, cell, model, treeiter, data=None):
    #     name = model.get_value(treeiter, 0)
    #     # if self.db.get_note_prop(idx, 'content'):
    #     #     title += '<i><span foreground=\'grey\'> ... </span></i>'
    #     # if '!' in title:
    #     text = '<b>' + name + '</b> \\ Bu'
    #     cell.set_property('markup', text)

    # def cell_data_fn_tags(self, column, cell, model, treeiter, data=None):
    #     pass
    #     #idx = model.get_value(treeiter, 0)
    #     #tags = self.db.get_note_prop(idx, 'tags')
    #     #cell.set_property('text', ', '.join(tags))

    # def cell_data_fn_utime(self, column, cell, model, treeiter, data=None):
    #     return
    #     idx = model.get_value(treeiter, 0)
    #     timestamp = self.db.get_note_prop(idx, 'utime')
    #     ts = float(timestamp)
    #     dt = datetime.fromtimestamp(ts)
    #     now = datetime.now()
    #     time_str = ''

    #     if dt.date() == now.date():          # today -> 'HH:MM'
    #         time_str = dt.strftime('%H:%M')
    #     elif dt.year == now.year:            # this year - > 'Month Day'
    #         time_str = dt.strftime('%b') + ' ' + str(dt.day)
    #     else:                                # before -> 'Month Day, Year'
    #         time_str = '%s %d, %d' % (dt.strftime('%b'), dt.day, dt.year)

    #cell.set_property('text', time_str)
