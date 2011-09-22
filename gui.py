#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime, timedelta
import gtk

from constants import COLORS
from devices import UE9, Virtual
import graphs
from modes import Match

GAMEMODES = ['Match', 'TimeAttack']
class Carrera(object):

    def __init__(self):
        self.device = UE9()
        self.builder = gtk.Builder()
        self.builder.add_from_file('gui.glade')
        self.builder.connect_signals(self)
        for i in range(2):
            self.add_player()
        gamemodes = gtk.combo_box_entry_new_text()
        gamemodes.child.connect('changed', self.on_gamemode_changed)
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

    def quit(self, *args, **kwargs):
        if hasattr(self, 'match'):
            self.match.cancel()
        gtk.main_quit()

    def add_player(self):
        if self.num_players == 4:
            return
        box = gtk.HBox()
        button = gtk.Button('', stock=gtk.STOCK_REMOVE)
        # small "hack" to get rid of the label
        button.get_children()[0].get_children()[0].get_children()[1].set_label('')
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
        self.clear_racewindow()
        if self.gamemode == 'Match':
            self.start_match()
        elif self.gamemode == 'TimeAttack':
            self.start_time_attack()

    def on_main_delete_event(self, obj, event):
        self.quit()

    def on_race_delete_event(self, obj, event):
        return True

    def on_gamemode_changed(self, obj):
        self.gamemode = obj.get_text()
        settings_box = self.builder.get_object('settings_box')
        for child in settings_box.children():
            settings_box.remove(child)
        if self.gamemode == 'Match':
            box = gtk.HBox()

            label = gtk.Label('Runden:')
            box.pack_start(label)
            label.show()

            adjustment = gtk.Adjustment(value=5, lower=0, upper=100, step_incr=1,
                                        page_incr=5)
            self.button_rounds_num = gtk.SpinButton(adjustment)
            box.pack_start(self.button_rounds_num)
            self.button_rounds_num.show()

            box.show()
            settings_box.pack_start(box, expand=False)
        elif self.gamemode == 'TimeAttack':
            box = gtk.HBox()

            label = gtk.Label('Sekunden:')
            box.pack_start(label)
            label.show()

            adjustment = gtk.Adjustment(value=180, lower=0, upper=3600, step_incr=30,
                                        page_incr=120)
            self.button_seconds = gtk.SpinButton(adjustment)
            box.pack_start(self.button_seconds)
            self.button_seconds.show()

            box.show()
            settings_box.pack_start(box, expand=False)

    def on_computer_speed_format_value(self, obj, value):
        self.device.computer_speed = min(4095, value * 856.695)

    on_power_on_0_clicked = lambda self, obj: self.power_on(0)
    on_power_off_0_clicked = lambda self, obj: self.power_off(0)
    on_power_on_1_clicked = lambda self, obj: self.power_on(1)
    on_power_off_1_clicked = lambda self, obj: self.power_off(1)
    on_power_on_2_clicked = lambda self, obj: self.power_on(2)
    on_power_off_2_clicked = lambda self, obj: self.power_off(2)
    on_power_on_3_clicked = lambda self, obj: self.power_on(3)
    on_power_off_3_clicked = lambda self, obj: self.power_off(3)
    on_power_on_all_clicked = lambda self, obj: self.power_on(-1)
    on_power_off_all_clicked = lambda self, obj: self.power_off(-1)


    def clear_racewindow(self):
        if hasattr(self, 'match'):
            self.match.cancel()
        for box in self.builder.get_object('race_box').children():
            self.builder.get_object('race_box').remove(box)
        try:
            canvas = self.builder.get_object('round_graph').children()[0]
            self.builder.get_object('round_graph').remove(canvas)
        except IndexError:
            pass

    @property
    def num_players(self):
        return len(self.builder.get_object('player_box').children())

    def power_on(self, track):
        self.device.power_on(track)

    def power_off(self, track):
        self.device.power_off(track)

    def start_match(self):
        race_box = self.builder.get_object('race_box')
        players = self.builder.get_object('player_box').children()
        if not 1 < self.num_players < 5:
            return
        rounds = int(self.button_rounds_num.get_value())
        for i, player in enumerate(players):
            vbox = gtk.VBox()

            playername = gtk.Label()
            playername.set_use_markup(True)
            playername.set_markup('<span size="18000" color="{0}">{1}</span>'.format(
                COLORS[i],
                player.children()[0].get_text()))
            vbox.add(playername)
            playername.show()

            round_ = gtk.Label()
            round_.set_use_markup(True)
            round_.set_markup('<span size="36000">1/{0}</span>'.format(rounds))
            vbox.add(round_)
            round_.show()

            race_box.add(vbox)
            vbox.show()

        self.match = Match(self.device, self.num_players, rounds=rounds)
        self.match.start()
        boxes = self.builder.get_object('race_box').children()
        last_times = [None] * self.num_players

        graph = graphs.Match(self.num_players, rounds=rounds)
        self.builder.get_object('round_graph').add(graph.canvas)
        graph.show()
        need_draw = True
        self.rank_counter = 1
        while not self.match.finished:
            while gtk.events_pending():
                gtk.main_iteration()
            self.match.poll()
            for i, box in enumerate(boxes):
                try:
                    if last_times[i] != self.match.player_times[i][-1]:
                        if len(self.match.player_times[i]) < rounds:
                            text = '<span size="36000">{0}/{1}</span>'.format(
                                len(self.match.player_times[i]) + 1, rounds)
                        else:
                            text = '<span size="36000">{0}.</span>'.format(
                                self.rank_counter)
                            self.rank_counter += 1
                        box.children()[1].set_markup(text)
                        graph.add(i, self.match.player_times[i][-1])
                        need_draw = True
                        last_times[i] = self.match.player_times[i][-1]
                except IndexError:
                    pass
            if need_draw:
                graph.draw()
                need_draw = False

    def start_time_attack(self):
        pass

if __name__ == '__main__':
    carrera = Carrera()
    carrera.run()
