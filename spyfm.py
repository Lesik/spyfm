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
        self.store = Gtk.ListStore(str, str)
        self.store.set_sort_func(0, self.sort_func, None)
        self.tree = Gtk.TreeView(self.store)
        scrolledwindow.add(self.tree)

        renderer = Gtk.CellRendererText()
        column_name = Gtk.TreeViewColumn("Name", renderer, text=0)
        column_name.set_sort_column_id(0)
        column_size = Gtk.TreeViewColumn("Size", renderer, text=1)
        self.tree.append_column(column_name)
        self.tree.append_column(column_size)
        self.tree.connect('row-activated', self.on_tree_row_activated)

        self.add(scrolledwindow)
        self.show_all()
        self.list()

    def sort_func(self, treemodel, iter1, iter2, user_data):
        sort_column, _ = treemodel.get_sort_column_id()
        item1 = treemodel.get_value(iter1, sort_column)
        item2 = treemodel.get_value(iter2, sort_column)

        path1 = join(self.currentdir, item1)
        path2 = join(self.currentdir, item2)

        if isdir(path1) ^ isdir(path2):
            if isdir(path1):
                return -1
            else:
                return 1
        else:
            if item1 < item2:
                return -1
            elif item1 == item2:
                return 0
            else:
                return 1

    def list(self):
        self.store.clear()
        for item in listdir(self.currentdir):
            path = join(self.currentdir, item)
            if not item.startswith("."):
                if isdir(path):
                    size = "Folder"
                else:
                    size = str(getsize(path)) + " bytes"
                self.store.append([item, size])

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
