import re
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from .version import VERSION
from .run_svn import run_svn
from .cache_file import CacheFile

class MainWindow(Gtk.Window):
    def __init__(self, url):
        super().__init__(title = "Simple SVN Browser v%s" % VERSION)

        self.repo_root = None
        self.cache_file = CacheFile()
        self.directory_buttons = []

        if (self.cache_file["width"] is not None and
                self.cache_file["height"] is not None):
            self.set_default_size(self.cache_file["width"],
                                  self.cache_file["height"])

        top_hbox = Gtk.Box()
        self.address_entry = Gtk.Entry(text = url)
        self.address_entry.connect("activate", self.on_go_button_clicked)
        self.go_button = Gtk.Button(label = "Go")
        self.go_button.connect("clicked", self.on_go_button_clicked)
        top_hbox.pack_start(self.address_entry, True, True, 0)
        top_hbox.pack_start(self.go_button, False, True, 0)

        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        vbox.pack_start(top_hbox, False, True, 0)

        bottom_hbox = Gtk.Box()
        self.directory_vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        bottom_hbox.pack_start(self.directory_vbox, False, True, 0)
        separator = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)
        bottom_hbox.pack_start(separator, False, True, 0)
        bottom_hbox.pack_start(Gtk.Label(label = "right placeholder"), True, True, 0)
        vbox.pack_start(bottom_hbox, True, True, 0)

        self.add(vbox)

        self.connect("delete-event", self.__close)
        self.show_all()

        if (self.cache_file["x"] is not None and
                self.cache_file["y"] is not None):
            self.move(self.cache_file["x"], self.cache_file["y"])

        self.__go(url)

    def run(self):
        Gtk.main()

    def on_go_button_clicked(self, widget):
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

    def __refresh(self, url):
        self.__refresh_repo_root(url)
        if self.repo_root is not None:
            self.__refresh_directory_buttons(url)
            self.__refresh_directory_contents(url)
        else:
            # TODO: invalidate bottom pane
            pass

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
                    self.directory_buttons[i].caption != caption):
                for btn in self.directory_buttons[i:]:
                    btn.destroy()
                self.directory_buttons[i:] = []
            if len(self.directory_buttons) <= i:
                btn = Gtk.Button(label = caption)
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
        # TODO: finish

    def __go(self, url):
        self.address_entry.set_text(url)
        self.on_go_button_clicked(self.go_button)
