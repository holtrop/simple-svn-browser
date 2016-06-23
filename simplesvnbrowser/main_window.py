import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from .version import VERSION
from .run_svn import run_svn
from .cache_file import CacheFile

class MainWindow(Gtk.Window):
    def __init__(self, url):
        super().__init__(title = "Simple SVN Browser v%s" % VERSION)

        self.cache_file = CacheFile()
        if (self.cache_file["width"] is not None and
                self.cache_file["height"] is not None):
            self.set_default_size(self.cache_file["width"],
                                  self.cache_file["height"])

        top_hbox = Gtk.Box()
        address_entry = Gtk.Entry(text = url)
        go_button = Gtk.Button(label = "Go")
        top_hbox.pack_start(address_entry, True, True, 0)
        top_hbox.pack_start(go_button, False, True, 0)

        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        vbox.pack_start(top_hbox, False, True, 0)

        bottom_hbox = Gtk.Box()
        self.directory_vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.directory_vbox.pack_start(Gtk.Label(label = "left placeholder"), False, True, 0)
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

    def run(self):
        Gtk.main()

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
