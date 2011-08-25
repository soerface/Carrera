#!/usr/bin/env python

import gtk

class Carrera(object):

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file('gui.glade')
        self.builder.connect_signals(self)

    def run(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass

    def quit(self):
        gtk.main_quit()

if __name__ == '__main__':
    carrera = Carrera()
    carrera.run()
