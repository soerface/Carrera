#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        button = gtk.Button('×')
        button.connect('clicked', self.on_remove_player_clicked)
        entry = gtk.Entry()
        entry.set_text('Nameless')
        box.pack_start(entry)
        box.pack_start(button, expand=False, padding=5)
        self.builder.get_object('player_box').pack_start(box, expand=False)
        button.show()
        entry.show()
        box.show()

    def on_add_player_clicked(self, obj):
        self.add_player()

    def on_remove_player_clicked(self, obj):
        row = obj.parent
        box = row.parent
        box.remove(row)

    def on_start_race_clicked(self, obj):
        race_box = self.builder.get_object('race_box')
        players = self.builder.get_object('player_box').children()
        if not 1 < self.num_players < 5:
            return
        rounds = 8
        for player in players:
            vbox = gtk.VBox()

            round_ = gtk.Label()
            round_.set_use_markup(True)
            round_.set_markup('<span size="36000">1/{0}</span>'.format(rounds))
            vbox.add(round_)
            round_.show()

            playername = gtk.Label()
            playername.set_use_markup(True)
            playername.set_markup('<span size="18000">{0}</span>'.format(
                player.children()[0].get_text()))
            vbox.add(playername)
            playername.show()

            race_box.add(vbox)
            vbox.show()

        device = Virtual()
        self.match = Match(device, self.num_players, rounds=rounds)
        self.match.start()
        boxes = self.builder.get_object('race_box').children()
        last_times = deepcopy(self.match.player_times)

        self.builder.get_object('main').hide()
        self.builder.get_object('race').show()

        while not self.match.finished:
            while gtk.events_pending():
                gtk.main_iteration()
            self.match.poll()
            if last_times != self.match.player_times:
                for i, box in enumerate(boxes):
                    if len(self.match.player_times[i]) < rounds:
                        text = '<span size="36000">{0}/{1}</span>'.format(
                            len(self.match.player_times[i]) + 1, rounds)
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

    @property
    def num_players(self):
        return len(self.builder.get_object('player_box').children())

if __name__ == '__main__':
    carrera = Carrera()
    carrera.run()
