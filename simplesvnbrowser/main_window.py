import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from .version import VERSION
from .run_svn import run_svn

class MainWindow(Gtk.Window):
    def __init__(self, url):
        super().__init__(title = "Simple SVN Browser v%s" % VERSION)

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

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def run(self):
        Gtk.main()
