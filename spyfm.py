#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from os import listdir
from os.path import expanduser, join, isdir, getsize

class SPyFM(Gtk.Window):

    currentdir = expanduser("~")

    def __init__(self):
        super().__init__(title="SPyFM")
        self.connect('delete-event', Gtk.main_quit)
        self.set_default_size(700, 700)

        scrolledwindow = Gtk.ScrolledWindow(None, None)
        self.store = Gtk.ListStore(str)
        self.tree = Gtk.TreeView(self.store)
        scrolledwindow.add(self.tree)

        renderer = Gtk.CellRendererText()
        column_name = Gtk.TreeViewColumn("Name", renderer, text=0)
        self.tree.append_column(column_name)
        self.tree.connect('row-activated', self.on_tree_row_activated)

        self.add(scrolledwindow)
        self.show_all()
        self.list()

    def list(self):
        self.store.clear()
        for item in listdir(self.currentdir):
            path = join(self.currentdir, item)
            if not item.startswith("."):
                self.store.append([item])

    def on_tree_row_activated(self, treeview, path, view_column):
        # TODO fully understand the following line
        path = join(self.currentdir,
            self.store.get_value(self.store.get_iter(path), 0))
        if isdir(path):
            self.currentdir = path
            self.list()

if __name__ == "__main__":
    SPyFM()
    Gtk.main()
