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

    def quit(self):
        gtk.main_quit()

    def add_player(self, *args):
        if self.num_players == 4:
            return
        self.num_players += 1
        box = gtk.combo_box_new_text()
        self.builder.get_object('player_box').add(box)
        box.show()

if __name__ == '__main__':
    carrera = Carrera()
    carrera.run()
