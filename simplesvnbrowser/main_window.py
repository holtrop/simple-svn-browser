import os
import re
import subprocess
import sys
import tempfile
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from .version import VERSION
from .run_svn import run_svn
from .cache_file import CacheFile

class MainWindow(Gtk.Window):
    def __init__(self, url):
        super().__init__(title = "Simple SVN Browser v%s" % VERSION)

        self.repo_root = None
        self.current_url = None
        self.cache_file = CacheFile()
        self.directory_buttons = []
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.url_history = []

        if (self.cache_file["width"] is not None and
                self.cache_file["height"] is not None):
            self.set_default_size(self.cache_file["width"],
                                  self.cache_file["height"])

        top_hbox = Gtk.Box()
        self.address_entry = Gtk.Entry(text = url)
        self.address_entry.connect("activate", self.__on_go_button_clicked)
        self.go_button = Gtk.Button(label = "Go")
        self.go_button.connect("clicked", self.__on_go_button_clicked)
        top_hbox.pack_start(self.address_entry, True, True, 0)
        top_hbox.pack_start(self.go_button, False, True, 0)

        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        vbox.pack_start(top_hbox, False, True, 0)

        self.contents_model = Gtk.ListStore(str, str)
        self.contents_treeview = Gtk.TreeView.new_with_model(self.contents_model)
        self.contents_treeview.set_headers_visible(False)
        self.contents_treeview.connect("row-activated", self.__on_contents_treeview_row_activated)
        self.contents_treeview.connect("button-release-event", self.__on_contents_treeview_button_press)
        self.contents_treeview.set_search_column(1)
        icon_renderer = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn("Icon", icon_renderer, icon_name = 0)
        self.contents_treeview.append_column(column)
        text_renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", text_renderer, text = 1)
        self.contents_treeview.append_column(column)

        contents_scrolledwindow = Gtk.ScrolledWindow()
        contents_scrolledwindow.set_vexpand(True)
        contents_scrolledwindow.add(self.contents_treeview)

        bottom_hbox = Gtk.Box()
        self.directory_vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        bottom_hbox.pack_start(self.directory_vbox, False, True, 0)
        separator = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)
        bottom_hbox.pack_start(separator, False, True, 0)
        bottom_hbox.pack_start(contents_scrolledwindow, True, True, 0)
        vbox.pack_start(bottom_hbox, True, True, 0)

        self.add(vbox)

        self.connect("delete-event", self.__close)
        self.connect("key-press-event", self.__on_key_press_event)

        icon_theme = Gtk.IconTheme.get_default()
        icon = icon_theme.load_icon("folder", 128, 0)
        self.set_icon(icon)

        self.__set_default_window_position()
        self.show_all()
        self.__set_default_window_position()

        self.__go(url)

    def run(self):
        Gtk.main()

    def __on_go_button_clicked(self, widget):
        self.__refresh(self.address_entry.get_text())
        return True

    def __close(self, *more):
        size = self.get_size()
        position = self.get_position()
        self.cache_file["width"] = size[0]
        self.cache_file["height"] = size[1]
        self.cache_file["x"] = position[0]
        self.cache_file["y"] = position[1]
        self.cache_file.write()
        Gtk.main_quit()
        return True

    def __set_default_window_position(self):
        if (self.cache_file["x"] is not None and
                self.cache_file["y"] is not None):
            self.move(self.cache_file["x"], self.cache_file["y"])

    def __refresh(self, url):
        url = re.sub(r'/+$', '', url)
        self.__refresh_repo_root(url)
        if self.repo_root is not None:
            self.current_url = url
            if len(self.url_history) < 1 or self.url_history[-1] != url:
                self.url_history.append(url)
            self.__refresh_directory_buttons(url)
            self.__refresh_directory_contents(url)
        else:
            for btn in self.directory_buttons:
                btn.destroy()
            self.directory_buttons = []
            self.contents_model.clear()

    def __refresh_repo_root(self, url):
        if (self.repo_root is not None and
                (url == self.repo_root or
                 url.startswith(self.repo_root + "/"))):
            # Up to date
            pass
        else:
            stdout, _ = run_svn(["info", url])
            m = re.search(r'^Repository Root: (.*)$', stdout, re.MULTILINE)
            if m is not None:
                self.repo_root = m.group(1)
            else:
                self.repo_root = None

    def __refresh_directory_buttons(self, url):
        if url == self.repo_root:
            path_in_repo = ""
        else:
            path_in_repo = url[len(self.repo_root):]
        path_parts = re.sub(r'/+', '/', path_in_repo).split('/')
        directory_url = self.repo_root
        for i, part in enumerate(path_parts):
            caption = part if i > 0 else "/"
            if part != "":
                directory_url += "/" + part
            if (len(self.directory_buttons) > i and
                    (self.directory_buttons[i].caption != caption or
                     self.directory_buttons[i].directory_url != directory_url)):
                for btn in self.directory_buttons[i:]:
                    btn.destroy()
                self.directory_buttons[i:] = []
            if len(self.directory_buttons) <= i:
                btn = Gtk.Button(label = caption)
                btn.get_child().set_xalign(0.0)
                btn.caption = caption
                btn.directory_url = directory_url
                handler = lambda widget: self.__go(widget.directory_url)
                btn.connect("clicked", handler)
                self.directory_vbox.pack_start(btn, False, False, 0)
                self.directory_buttons.append(btn)
        for i, btn in enumerate(self.directory_buttons):
            if i == len(path_parts) - 1:
                btn.get_child().set_markup("<b>%s</b>" % btn.caption)
            else:
                btn.get_child().set_label(btn.caption)
        self.directory_vbox.show_all()

    def __refresh_directory_contents(self, url):
        stdout, _ = run_svn(["ls", url])
        self.contents_model.clear()
        for line in stdout.split("\n"):
            entry_name = line.rstrip("\r\n")
            if entry_name == "":
                continue
            folder = False
            m = re.match(r'(.*)/', entry_name)
            if m is not None:
                entry_name = m.group(1)
                folder = True
            self.contents_model.append(("folder" if folder else "text-x-generic", entry_name))

    def __go(self, url):
        self.address_entry.set_text(url)
        self.__on_go_button_clicked(self.go_button)

    def __on_contents_treeview_row_activated(self, widget, path, column):
        model_iterator = self.contents_model.get_iter(path)
        entry_type = self.contents_model.get_value(model_iterator, 0)
        entry_name = self.contents_model.get_value(model_iterator, 1)
        entry_url = self.current_url + "/" + entry_name
        if entry_type == "folder":
            self.__go(entry_url)
        else:
            self.__activate_file(entry_url)

    def __activate_file(self, url):
        with tempfile.NamedTemporaryFile(suffix = "-" + os.path.basename(url)) as f:
            temp_fname = f.name
        run_svn(["export", url, temp_fname])
        if os.path.exists(temp_fname):
            subprocess.run(["xdg-open", temp_fname])
        else:
            sys.stderr.write("Unable to export file.\n")

    def __on_contents_treeview_button_press(self, widget, event):
        if event.button == 3:
            selected_iterator = self.contents_treeview.get_selection().get_selected()
            if selected_iterator is not None and selected_iterator[1] is not None:
                entry_name = selected_iterator[0].get_value(selected_iterator[1], 1)
                entry_url = self.current_url + "/" + entry_name
                self.popup_menu = Gtk.Menu()
                mi = Gtk.MenuItem(label = "Copy URL")
                handler = lambda widget: self.clipboard.set_text(entry_url, -1)
                mi.connect("activate", handler)
                self.popup_menu.append(mi)
                self.popup_menu.show_all()
                self.popup_menu.popup(None, None, None, None, event.button, event.time)

    def __on_key_press_event(self, widget, event):
        if event.keyval == Gdk.keyval_from_name("Back"):
            if len(self.url_history) >= 2:
                self.url_history.pop()
                self.__go(self.url_history.pop())
            return True
        return False
