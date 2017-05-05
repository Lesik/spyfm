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

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # passing None to Gtk.ScrolledWindow constructor according to docs:
        # https://developer.gnome.org/gtk3/stable/GtkScrolledWindow.html#gtk-scrolled-window-new
        scrolledwindow = Gtk.ScrolledWindow(None, None)
        self.store = Gtk.ListStore(str, str)
        self.store.set_sort_func(0, self.sort_func, None)
        self.tree = Gtk.TreeView(self.store)
        scrolledwindow.add(self.tree)
        box.pack_end(scrolledwindow, True, True, 0)

        entry_path = Gtk.Entry()
        entry_path.set_text(self.currentdir)
        entry_path.connect('activate', self.on_entry_path_activated)
        box.pack_start(entry_path, False, False, 0)

        renderer = Gtk.CellRendererText()
        column_name = Gtk.TreeViewColumn("Name", renderer, text=0)
        column_name.set_sort_column_id(0)
        column_size = Gtk.TreeViewColumn("Size", renderer, text=1)
        self.tree.append_column(column_name)
        self.tree.append_column(column_size)
        self.tree.connect('row-activated', self.on_tree_row_activated)

        self.add(box)
        self.show_all()
        self.list()

    def on_entry_path_activated(self, entry):
        if isdir(entry.get_text()):
            self.currentdir = entry.get_text()
            self.list()
        else:
            entry.set_text(self.currentdir)

    def sort_func(self, treemodel, iter1, iter2, user_data):
        sort_column, _ = treemodel.get_sort_column_id()
        item1 = treemodel.get_value(iter1, sort_column)
        item2 = treemodel.get_value(iter2, sort_column)

        path1 = join(self.currentdir, item1)
        path2 = join(self.currentdir, item2)

        # if either path1 or path2 is folder but not both
        if isdir(path1) ^ isdir(path2):
            # show the folder first
            if isdir(path1):
                return -1
            else:
                return 1
        # else either both or none of them are folders
        else:
            # do normal sorting
            if item1 < item2:
                return -1
            elif item1 == item2:
                return 0
            else:
                return 1

    def list(self):
        # clear previous items, if any
        self.store.clear()
        for item in listdir(self.currentdir):
            path = join(self.currentdir, item)
            # do not show hidden files
            if not item.startswith("."):
                # do not calculate size for folders
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
