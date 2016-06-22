import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from .version import VERSION
from .run_svn import run_svn

class MainWindow(Gtk.Window):
    def __init__(self, url):
        super().__init__(title = "Simple SVN Browser v%s" % VERSION)

        button = Gtk.Button(label = "content")
        self.add(button)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def run(self):
        Gtk.main()
