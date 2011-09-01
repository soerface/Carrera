#!/usr/bin/env python

import gtk

GAMEMODES = ['Match']
class Carrera(object):

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file('gui.glade')
        self.builder.connect_signals(self)
        self.num_players = 0
        self.add_player()
        gamemodes = gtk.combo_box_new_text()
        for text in GAMEMODES:
            gamemodes.append_text(text)
        gamemodes.set_active(0)
        self.builder.get_object('modes_box').add(gamemodes)
        gamemodes.show()

    def run(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass

    def quit(self, *args):
        gtk.main_quit()

    def add_player(self, *args):
        if self.num_players == 4:
            return
        box = gtk.HBox()
        button = gtk.Button()
        button.connect('clicked', self.remove_player)
        entry = gtk.Entry()
        box.add(entry)
        box.add(button)
        self.builder.get_object('player_box').add(box)
        button.show()
        entry.show()
        box.show()
        self.num_players += 1

    def remove_player(self, obj):
        row = obj.parent
        box = row.parent
        box.remove(row)
        self.num_players -= 1

if __name__ == '__main__':
    carrera = Carrera()
    carrera.run()
