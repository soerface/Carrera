#!/usr/bin/env python

from copy import deepcopy
from datetime import datetime, timedelta
import gtk

from devices import UE9, Virtual
import graphs
from modes import Match

GAMEMODES = ['Match']
class Carrera(object):

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file('gui.glade')
        self.builder.connect_signals(self)
        self.num_players = 0
        for i in range(2):
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

    def add_player(self):
        if self.num_players == 4:
            return
        box = gtk.HBox()
        button = gtk.Button()
        button.connect('clicked', self.on_remove_player_clicked)
        entry = gtk.Entry()
        box.add(entry)
        box.add(button)
        self.builder.get_object('player_box').add(box)
        button.show()
        entry.show()
        box.show()
        self.num_players += 1

    def on_add_player_clicked(self, obj):
        self.add_player()

    def on_remove_player_clicked(self, obj):
        row = obj.parent
        box = row.parent
        box.remove(row)
        self.num_players -= 1

    def on_start_race_clicked(self, obj):
        self.builder.get_object('main').hide()
        self.builder.get_object('race').show()
        race_box = self.builder.get_object('race_box')
        players = self.builder.get_object('player_box').children()
        for player in players:
            vbox = gtk.VBox()

            round_ = gtk.Label()
            round_.set_use_markup(True)
            round_.set_markup('<span size="36000">1</span>')
            vbox.add(round_)
            round_.show()

            playername = gtk.Label()
            playername.set_use_markup(True)
            playername.set_markup('<span size="18000">{0}</span>'.format(
                player.children()[0].get_text())
            )
            vbox.add(playername)
            playername.show()

            race_box.add(vbox)
            vbox.show()

        device = Virtual()
        rounds = 8
        self.match = Match(device, len(players), rounds=rounds)
        self.match.start()
        boxes = self.builder.get_object('race_box').children()
        last_times = deepcopy(self.match.player_times)
        while not self.match.finished:
            while gtk.events_pending():
                gtk.main_iteration()
            self.match.poll()
            if last_times != self.match.player_times:
                for i, box in enumerate(boxes):
                    if len(self.match.player_times[i]) < rounds:
                        text = '<span size="36000">{0}</span>'.format(
                            len(self.match.player_times[i]) + 1
                        )
                    else:
                        text = '<span size="36000">:)</span>'
                    box.children()[0].set_markup(text)
                last_times = deepcopy(self.match.player_times)
        if not self.match.canceled:
            graph = graphs.Rounds()
            for i, times in enumerate(self.match.player_times):
                graph.add(times)
                for j, time in enumerate(times):
                    pass#print '  Runde {0}: {1}'.format(j+1, time)
            self.builder.get_object('round_graph').add(graph.canvas)
            graph.show()

    def on_main_delete_event(self, obj, event):
        self.quit()

    def on_race_delete_event(self, obj, event):
        self.match.cancel()
        for box in self.builder.get_object('race_box').children():
            self.builder.get_object('race_box').remove(box)
        try:
            canvas = self.builder.get_object('round_graph').children()[0]
            self.builder.get_object('round_graph').remove(canvas)
        except IndexError:
            pass
        self.builder.get_object('race') .hide()
        self.builder.get_object('main').show()
        return True

if __name__ == '__main__':
    carrera = Carrera()
    carrera.run()
