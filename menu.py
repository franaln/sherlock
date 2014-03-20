import sys, math, cairo
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject

white = (1.0, 1.0, 1.0)

query_color = (0.1, 0.1, 0.1)
title_color = (0.1, 0.1, 0.1) # #030303
subtitle_color = (0.2, 0.2, 0.2) # #050505

bkg_color      = (0.92, 0.92, 0.92) # #ebebeb
selected_color = (0.259, 0.498, 0.929) # #427fed
entry_color    = (0.8, 0.8, 0.8) # #141414
line_color     = (0.8, 0.8, 0.8)

# def add_background(pixbuf, color=0xebebebff):
#     """ adds a background with given color to
#     the pixbuf and returns the result as new Pixbuf"""
#     result = GdkPixbuf.Pixbuf().new(pixbuf.get_colorspace(),
#                                     True,
#                                     pixbuf.get_bits_per_sample(),
#                                     pixbuf.get_width(),
#                                     pixbuf.get_height(),
#     )
#     result.fill(color)
#     pixbuf.composite(result, 0, 0,
#                      pixbuf.get_width(), pixbuf.get_height(),
#                      0, 0,
#                      1, 1,
#                      GdkPixbuf.InterpType.NEAREST,
#                      255)
#     return result

class Menu(Gtk.Window, GObject.GObject):

    __gsignals__ = {
        'query_changed': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    def __init__(self):

        # config
        self.width = 480
        self.height = 60

        self.offset = 6
        self.bar_width  = self.width - self.offset * 2
        self.bar_height = self.height - self.offset * 2
        self.item_height = 48

        self.lines = 5
        self.max_items = 20

        # data
        self.items = []
        self.actions = []
        self.selected = 0
        self.query = ''

        GObject.GObject.__init__(self)
        super().__init__(type=Gtk.WindowType.TOPLEVEL)

        self.set_app_paintable(True)
        self.set_decorated(False)
        #self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)

        self.set_title('Sherlock')

        self.set_size_request(self.width, self.height)

        self.connect('draw', self.draw)
        self.connect('screen-changed', self.screen_changed)

        self.screen_changed(self)
        self.show_all()

    def get_selected(self):
        return self.selected

    def show(self, items):
        self.items = list(items)
        self.show_box()

    def clear(self):
        self.items = []
        self.selected = 0
        self.hide_box()

    def show_box(self):
        self.resize(self.width, self.height+self.item_height * self.lines)
        self.queue_draw()

    def hide_box(self):
        self.resize(self.width, self.height)
        self.queue_draw()

    def add_char(self, char):
        self.query += char
        self.queue_draw()
        self.emit('query_changed', self.query)

    def rm_char(self):
        self.query = self.query[:-1]
        self.queue_draw()
        self.emit('query_changed', self.query)

    def do_query_changed(self, entry):
        self.waiting = False

    def show_actions(self):
        #if self.items.
        pass


    def draw_rect(self, cr, x, y, width, height, color):
        cr.set_source_rgb(*color)
        cr.rectangle(x, y, width, height)
        cr.fill()

    def draw_text(self, cr, x, y, text, color, size=14):
        cr.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(size)

        descent, font_height = cr.font_extents()[1:3]

        print(text)
        (x_bearing, y_bearing, text_width, text_height) = cr.text_extents(text)[:4]

        y = y - descent + font_height / 2

        cr.move_to(x, y)
        cr.set_source_rgb(*color)
        cr.show_text(text)


    def draw(self, widget, event):
        # get cairo context
        cr = Gdk.cairo_create(widget.get_window())

        # draw window rectangle
        cr.set_source_rgb(*bkg_color)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        # draw search entry
        self.draw_rect(cr, self.offset, self.offset, self.bar_width,
                       self.bar_height, entry_color)
        self.draw_text(cr, self.offset + 10, self.offset + self.bar_height/2,
                       self.query, query_color, 32)

        # cursor
        # cr. move_to(self.offset + 15 + width, self.offset + self.bar_height - 2)
        # cr.set_source_rgb(*query_color)
        # cr.set_line_width(0.8)
        # cr.line_to(self.offset + 15 + width, self.offset + 2)
        # cr.stroke()


        # draw items box if there are items to show
        if not self.items:
            return

        first_item =  0 if (self.selected < self.lines) else (self.selected - self.lines + 1)
        max_items = min(self.lines, len(self.items))

        for i in range(max_items):
            self.draw_item(cr, i, self.items[first_item+i], (first_item+i == self.selected))

        return False

    def draw_item(self, cr, pos, item, selected):

        """
        ----------------------------------------
        | icon | title                 |       |
        |      | subtitle              |       |
        ----------------------------------------
        """

        # pos to (x, y)
        base_x = 0
        base_y = self.height + pos * self.item_height

        # horizontal line below
        y = base_y + self.item_height - 1
        cr. move_to(10, y)
        cr.set_source_rgb(*line_color)
        cr.set_line_width(0.8)
        cr.line_to(self.width-10, y)
        cr.stroke()

        # selected background
        if selected:
            self.draw_rect(cr, base_x, base_y, self.width, self.item_height, selected_color)

        # icon (not icon for now!)
        #x = base_x + 5
        #y = base_y + (self.item_height - 40) / 2

        #icon_size = 40

        #cr.save()
        #cr.translate(x, y)

        #cr.rectangle(0, 0, icon_size, icon_size)
        #cr.clip ()

        # name = '/usr/share/icons/hicolor/48x48/apps/evince.png'
        # pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(item.icon, icon_size, icon_size)
        # pixbuf = add_background(pixbuf)

        # Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        # cr.paint()

        #cr.restore()

        # title
        x = base_x + 10 #+ 60
        y = base_y + self.item_height * (3/8)
        if selected:
            self.draw_text(cr, x, y, item.title, (1, 1, 1))
        else:
            self.draw_text(cr, x, y, item.title, title_color)

        # subtitle
        x = base_x + 10 #+ 60
        y = base_y + (3/4) * self.item_height
        if selected:
            self.draw_text(cr, x, y, item.subtitle, (1, 1, 1), 10)
        else:
            self.draw_text(cr, x, y, item.subtitle, subtitle_color, 10)


        # if selected:
        #     default_action = 'Open'
        #     cr.set_font_size(10)
        #     text_width = cr.text_extents(default_action)[2]

        #     self.draw_text(cr, self.width-text_width-30, y, default_action, self.nf_color, 10)

        #     cr.set_source_rgb(*self.nf_color)
        #     cr.set_line_width(1.5)
        #     cr.move_to(self.width-10, y + self.item_height/2+4)
        #     cr.rel_line_to(4, -4)
        #     cr.rel_line_to(-4, -4)
        #     cr.set_line_join(cairo.LINE_JOIN_ROUND)
        #     cr.stroke()


    def select_next(self):
        if self.selected == len(self.items) - 1:
            return
        self.selected += 1
        self.queue_draw()

    def select_prev(self):
        if self.selected == 0:
            self.hide_box()
            return
        self.selected -= 1
        self.queue_draw()

    def screen_changed(self, widget, old_screen=None):
        """ If screen changes, it could be possible
        we no longer got rgba colors """
        screen = widget.get_screen()
        visual = screen.get_rgba_visual()
        if visual is None:
            visual = screen.get_rgba_visual()
            self.supports_alpha = False
        else:
            self.supports_alpha = True

        widget.set_visual(visual)
        return True




# static void
        # show_cursor (GtkEntry *entry)
        # {
        #     GtkEntryPrivate *priv = entry->priv;
        #     GtkWidget *widget;

        #     if (!priv->cursor_visible)
        #     {
        #         priv->cursor_visible = TRUE;

        #         widget = GTK_WIDGET (entry);
        #         if (gtk_widget_has_focus (widget) && priv->selection_bound == priv->current_pos)
        #         gtk_widget_queue_draw (widget);
        #     }
        # }

        # static void
        # hide_cursor (GtkEntry *entry)
        # {
        #     GtkEntryPrivate *priv = entry->priv;
        #     GtkWidget *widget;

        #     if (priv->cursor_visible)
        #     {
        #         priv->cursor_visible = FALSE;

        #         widget = GTK_WIDGET (entry);
        #         if (gtk_widget_has_focus (widget) && priv->selection_bound == priv->current_pos)
        #         gtk_widget_queue_draw (widget);
        #     }
        # }

        #         /*
#         * Blink!
#         */
#         static gint
#         blink_cb (gpointer data)
#         {
#             GtkEntry *entry;
#             GtkEntryPrivate *priv;
#             gint blink_timeout;

#             entry = GTK_ENTRY (data);
#             priv = entry->priv;

#             if (!gtk_widget_has_focus (GTK_WIDGET (entry)))
#             {
#                 g_warning ("GtkEntry - did not receive focus-out-event. If you\n"
#                            "connect a handler to this signal, it must return\n"
#                            "FALSE so the entry gets the event as well");

#                 gtk_entry_check_cursor_blink (entry);

#                 return FALSE;
#             }

#             g_assert (priv->selection_bound == priv->current_pos);

#             blink_timeout = get_cursor_blink_timeout (entry);
#             if (priv->blink_time > 1000 * blink_timeout &&
#                 blink_timeout < G_MAXINT/1000)
#             {
#                       /* we've blinked enough without the user doing anything, stop blinking */
#       show_cursor (entry);
#       priv->blink_timeout = 0;
#     }
#   else if (priv->cursor_visible)
#     {
#       hide_cursor (entry);
#       priv->blink_timeout = gdk_threads_add_timeout (get_cursor_time (entry) * CURSOR_OFF_MULTIPLIER / CURSOR_DIVIDER,
#             blink_cb,
#             entry);
#       g_source_set_name_by_id (priv->blink_timeout, "[gtk+] blink_cb");
#     }
#   else
#     {
#       show_cursor (entry);
#       priv->blink_time += get_cursor_time (entry);
#       priv->blink_timeout = gdk_threads_add_timeout (get_cursor_time (entry) * CURSOR_ON_MULTIPLIER / CURSOR_DIVIDER,
#             blink_cb,
#             entry);
#       g_source_set_name_by_id (priv->blink_timeout, "[gtk+] blink_cb");
#     }

#   /* Remove ourselves */
#   return FALSE;
# }

# gtk_entry_check_cursor_blink (GtkEntry *entry)
        # {
        #     GtkEntryPrivate *priv = entry->priv;

        #     if (cursor_blinks (entry))
        #     {
        #         if (!priv->blink_timeout)
        #         {
        #             show_cursor (entry);
        #             priv->blink_timeout = gdk_threads_add_timeout (get_cursor_time (entry) * CURSOR_ON_MULTIPLIER / CURSOR_DIVIDER,
        #                                                            blink_cb,
        #                                                            entry);
        #             g_source_set_name_by_id (priv->blink_timeout, "[gtk+] blink_cb");
        #         }
        #     }
        #     else
        #     {
        #         if (priv->blink_timeout)
        #         {
        #             g_source_remove (priv->blink_timeout);
        #             priv->blink_timeout = 0;
        #         }

        #         priv->cursor_visible = TRUE;
        #     }
        # }

        # static void
        # gtk_entry_pend_cursor_blink (GtkEntry *entry)
        # {
        #     GtkEntryPrivate *priv = entry->priv;

        #     if (cursor_blinks (entry))
        #     {
        #         if (priv->blink_timeout != 0)
        #         g_source_remove (priv->blink_timeout);

        #         priv->blink_timeout = gdk_threads_add_timeout (get_cursor_time (entry) * CURSOR_PEND_MULTIPLIER / CURSOR_DIVIDER,
        #                                                        blink_cb,
        #                                                        entry);
        #         g_source_set_name_by_id (priv->blink_timeout, "[gtk+] blink_cb");
        #         show_cursor (entry);
        #     }
        # }

        # static void
        # gtk_entry_reset_blink_time (GtkEntry *entry)
        # {
        #     GtkEntryPrivate *priv = entry->priv;

        #     priv->blink_time = 0;
        # }


        # static void
        # gtk_entry_draw_text (GtkEntry *entry,
        #                      cairo_t  *cr)
        # {
        #     GtkEntryPrivate *priv = entry->priv;
        #     GtkWidget *widget = GTK_WIDGET (entry);
        #     GtkStateFlags state = 0;
        #     GdkRGBA text_color, bar_text_color;
        #     GtkStyleContext *context;
        #     gint width, height;
        #     gint progress_x, progress_y, progress_width, progress_height;
        #     gint clip_width, clip_height;

        #     /* Nothing to display at all */
        #     if (gtk_entry_get_display_mode (entry) == DISPLAY_BLANK)
        #     return;

        #     state = gtk_widget_get_state_flags (widget);
        #     context = gtk_widget_get_style_context (widget);

        #     gtk_style_context_get_color (context, state, &text_color);

        #     /* Get foreground color for progressbars */
        #     gtk_entry_prepare_context_for_progress (entry, context);
        #     gtk_style_context_get_color (context, state, &bar_text_color);
        #     gtk_style_context_restore (context);

        #     get_progress_area (widget,
        #                        &progress_x, &progress_y,
        #                        &progress_width, &progress_height);

        #     cairo_save (cr);

        #     clip_width = gdk_window_get_width (priv->text_area);
        #     clip_height = gdk_window_get_height (priv->text_area);
        #     cairo_rectangle (cr, 0, 0, clip_width, clip_height);
        #     cairo_clip (cr);

        #     /* If the color is the same, or the progress area has a zero
        #     * size, then we only need to draw once. */
        #     if (gdk_rgba_equal (&text_color, &bar_text_color) ||
        #         ((progress_width == 0) || (progress_height == 0)))
        #     {
        #         draw_text_with_color (entry, cr, &text_color);
        #     }
        #     else
        #     {
        #         int frame_x, frame_y, area_x, area_y;

        #         width = gdk_window_get_width (priv->text_area);
        #         height = gdk_window_get_height (priv->text_area);

        #         cairo_save (cr);

        #         cairo_set_fill_rule (cr, CAIRO_FILL_RULE_EVEN_ODD);
        #         cairo_rectangle (cr, 0, 0, width, height);

        #         /* progres area is frame-relative, we need it text-area window
        #         * relative */
        #         get_frame_size (entry, TRUE, &frame_x, &frame_y, NULL, NULL);
        #         gdk_window_get_position (priv->text_area, &area_x, &area_y);
        #         progress_x += frame_x - area_x;
        #         progress_y += frame_y - area_y;

        #         cairo_rectangle (cr, progress_x, progress_y,
        #                          progress_width, progress_height);
        #         cairo_clip (cr);
        #         cairo_set_fill_rule (cr, CAIRO_FILL_RULE_WINDING);

        #         draw_text_with_color (entry, cr, &text_color);
        #         cairo_restore (cr);

        #         cairo_save (cr);

        #         cairo_rectangle (cr, progress_x, progress_y,
        #                          progress_width, progress_height);
        #         cairo_clip (cr);

        #         draw_text_with_color (entry, cr, &bar_text_color);

        #         cairo_restore (cr);
        #     }

        #     cairo_restore (cr);
        # }

        # static void
        # gtk_entry_draw_cursor (GtkEntry  *entry,
        #                        cairo_t   *cr,
        #                        CursorType type)
        # {
        #     GtkEntryPrivate *priv = entry->priv;
        #     GtkWidget *widget = GTK_WIDGET (entry);
        #     GtkStyleContext *context;
        #     PangoRectangle cursor_rect;
        #     gint cursor_index;
        #     gboolean block;
        #     gboolean block_at_line_end;
        #     PangoLayout *layout;
        #     const char *text;
        #     gint x, y;

        #     context = gtk_widget_get_style_context (widget);

        #     layout = gtk_entry_ensure_layout (entry, TRUE);
        #     text = pango_layout_get_text (layout);
        #     get_layout_position (entry, &x, &y);

        #     if (type == CURSOR_DND)
        #     cursor_index = g_utf8_offset_to_pointer (text, priv->dnd_position) - text;
        #     else
        #     cursor_index = g_utf8_offset_to_pointer (text, priv->current_pos + priv->preedit_cursor) - text;

        #     if (!priv->overwrite_mode)
        #     block = FALSE;
        #     else
        #     block = _gtk_text_util_get_block_cursor_location (layout,
        #                                                       cursor_index, &cursor_rect, &block_at_line_end);

        #     if (!block)
        #     {
        #         gtk_render_insertion_cursor (context, cr,
        #                                      x, y,
        #                                      layout, cursor_index, priv->resolved_dir);
        #     }
        #     else /* overwrite_mode */
        #     {
        #         GdkRGBA cursor_color;
        #         GdkRectangle rect;

        #         cairo_save (cr);

        #         rect.x = PANGO_PIXELS (cursor_rect.x) + x;
        #         rect.y = PANGO_PIXELS (cursor_rect.y) + y;
        #         rect.width = PANGO_PIXELS (cursor_rect.width);
        #         rect.height = PANGO_PIXELS (cursor_rect.height);

        #         _gtk_style_context_get_cursor_color (context, &cursor_color, NULL);
        #         gdk_cairo_set_source_rgba (cr, &cursor_color);
        #         gdk_cairo_rectangle (cr, &rect);
        #         cairo_fill (cr);

        #         if (!block_at_line_end)
        #         {
        #             GtkStateFlags state;
        #             GdkRGBA color;

        #             state = gtk_widget_get_state_flags (widget);
        #             gtk_style_context_get_background_color (context, state, &color);

        #             gdk_cairo_rectangle (cr, &rect);
        #             cairo_clip (cr);
        #             cairo_move_to (cr, x, y);
        #             gdk_cairo_set_source_rgba (cr, &color);
        #             pango_cairo_show_layout (cr, layout);
        #         }

        #         cairo_restore (cr);
        #     }
        # }
