#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from itertools import izip, count

import gtk
from jinja2 import Environment, FileSystemLoader
import LabJackPython

from constants import COLORS, GAMEMODES
from devices import UE9, Virtual
import graphs
from modes import Match, TimeAttack, KnockOut, Training
from misc import Player
from utils import trim_time

class Carrera(object):
    """Class which handles the GTK interface."""

    def __init__(self):
        self.jinja_env = Environment(loader=FileSystemLoader('templates'))
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
        self.builder.get_object('banner').set_from_file('images/banner.png')
        try:
            self.device = UE9()
            self.builder.get_object('race').show()
            self.builder.get_object('main').present()
        except LabJackPython.NullHandleException, e:
            # fallback if no UE9 is connected
            self.device = Virtual()
            self.builder.get_object('simulation_warning').show()

    def run(self):
        """Display the GUI and start the mainloop."""
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass

    def quit(self, *args, **kwargs):
        """Quit the GUI and cancel any running race."""
        if hasattr(self, 'mode'):
            self.mode.cancel()
        gtk.main_quit()

    def add_player(self):
        """Add a new player box to the player list."""
        if len(self.player_names) == 3:
            self.builder.get_object('add_player').set_sensitive(False)
        elif len(self.player_names) == 4:
            return
        box = gtk.HBox()
        button = gtk.Button('', stock=gtk.STOCK_REMOVE)
        button.connect('clicked', self.on_remove_player_clicked)
        entry = gtk.Entry()
        entry.set_text('Nameless')
        box.pack_start(entry)
        box.pack_start(button, expand=False, padding=5)
        self.builder.get_object('player_box').pack_start(box, expand=False)
        button.show()
        entry.show()
        box.show()

    def draw_page(self, operation, context, page_nr):
        """Formats the page for printing."""

        current_time = datetime.now().strftime('%d.%m.%Y %H:%M'),
        layout = context.create_pango_layout()
        if self.last_gamemode == 'Match':
            template = self.jinja_env.get_template('match')
            best_round = {
                'time': trim_time(self.mode.best_round['time']),
                'player': self.last_players[self.mode.best_round['player_id']],
            }
            layout.set_markup(template.render(
                current_time = current_time,
                players = self.last_players,
                total_times = self.mode.total_times,
                worst_time = max(self.mode.total_times),
                best_round = best_round,
                round_num = self.mode.rounds,
                round_times = self.mode.round_times,
                )
            )
        elif self.last_gamemode == 'TimeAttack':
            template = self.jinja_env.get_template('timeattack')
            layout.set_markup(template.render(
                current_time = current_time,
                players = self.last_players,
                total_time = self.mode.seconds,
                )
            )
        cairo_context = context.get_cairo_context()
        cairo_context.show_layout(layout)

    def lock_settings(self, state):
        """(De)activates interface elements like player names"""
        state = False if state else True
        elements = ['add_player'] + ['start_race'] if self.gamemode != 'Training' else []
        for element in elements:
            self.builder.get_object(element).set_sensitive(state)
        elements = ['settings_box'] + ['player_box'] if self.gamemode != 'Training' else []
        for element in elements:
            for child in self.builder.get_object(element).children():
                for subchild in child.children():
                    subchild.set_sensitive(state)
        for child in self.builder.get_object('modes_box').children():
            child.set_sensitive(state)
        self.builder.get_object('cancel_race').set_sensitive(not state)

    def on_cancel_race_clicked(self, obj):
        self.mode.cancel()
        self.clear_racewindow()

    def on_simulation_warning_ok_clicked(self, obj):
        self.builder.get_object('simulation_warning').hide()
        self.builder.get_object('race').show()
        self.builder.get_object('main').present()

    def on_print_item_clicked(self, obj):
        print_op = gtk.PrintOperation()
        print_op.set_n_pages(1)
        print_op.connect('draw_page', self.draw_page)
        print_op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, None)

    def on_add_player_clicked(self, obj):
        self.add_player()

    def on_remove_player_clicked(self, obj):
        row = obj.parent
        box = row.parent
        box.remove(row)
        self.builder.get_object('add_player').set_sensitive(True)

    def on_start_race_clicked(self, obj):
        self.clear_racewindow()
        self.lock_settings(True)
        for i, color, player_name in izip(count(), COLORS, self.player_names):
            label = self.builder.get_object('player_label_{0:d}'.format(i))
            markup = '<span size="30000" color="{0}">{1}</span>'.format(
                color, player_name
            )
            label.set_markup(markup)

        self.players = [Player(i, self.device, name) for i, name in enumerate(self.player_names)]

        if self.gamemode == 'Match':
            rounds = int(self.button_rounds_num.get_value())
            condition = 'Absolviere als erster {0:d} Runden'.format(rounds)
            self.mode = Match(self.device, self, self.players, rounds=rounds)

        elif self.gamemode == 'TimeAttack':
            seconds = int(self.button_seconds.get_value())
            condition = 'Fahre soviele Runden wie möglich in {0:d} Sekunden'.format(seconds)
            self.mode = TimeAttack(self.device, self, self.players, seconds=seconds)

        elif self.gamemode == 'KnockOut':
            condition = 'Überlebe als letzer'
            self.mode = TimeAttack(self.device, self, self.players)

        elif self.gamemode == 'Training':
            rounds = int(self.button_rounds_num.get_value())
            condition = 'Training: {0:d} Runden pro Spur'.format(rounds)
            self.mode = Training(self.device, self, self.players, rounds)

        self.builder.get_object('condition_label').set_text(condition)
        self.mode.run()
        self.finish_race()

    def on_main_delete_event(self, obj, event):
        self.quit()

    def on_race_delete_event(self, obj, event):
        return True

    def on_gamemode_changed(self, obj):
        self.gamemode = obj.get_text()
        settings_box = self.builder.get_object('settings_box')
        for child in settings_box.children():
            settings_box.remove(child)
        if self.gamemode in ['Match', 'Training']:
            box = gtk.HBox()

            label = gtk.Label('Runden:')
            box.pack_start(label)
            label.show()

            adjustment = gtk.Adjustment(value=5, lower=1, upper=30, step_incr=1,
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

        self.builder.get_object('add_player').set_sensitive(
            self.gamemode != 'Training' and len(self.player_names) < 4)
        for child in self.builder.get_object('player_box').children():
            for subchild in child.children():
                subchild.set_sensitive(self.gamemode != 'Training')

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
        """Clear the racewindow

        Removes any infromation from the racewindow to provide a clean
        interface

        """
        self.builder.get_object('print_item').set_sensitive(False)
        for i in range(4):
            for label in ['player', 'total_time', 'best_round', 'rounds', 'rank']:
                obj = '{0}_label_{1}'.format(label, i)
                self.builder.get_object(obj).set_markup('<span size="30000">-</span>')
            self.builder.get_object('condition_label').set_text('-')
        return

    @property
    def player_names(self):
        """Returns a list of playernames."""
        children = self.builder.get_object('player_box').children()
        return [child.children()[0].get_text() for child in children]

    def power_on(self, track):
        """Power the given track on. Pass -1 to power all on"""
        self.device.power_on(track)

    def power_off(self, track):
        """Power the given track off. Pass -1 to power all off"""
        self.device.power_off(track)

    def finish_race(self):
        """Sets some final settings after a race and unlocks interface."""
        self.last_gamemode = self.gamemode
        self.last_players = self.player_names
        self.builder.get_object('print_item').set_sensitive(True)
        self.lock_settings(False)

    def update(self):
        """Called by gamemode to update interface"""
        while gtk.events_pending():
            gtk.main_iteration()
        if self.mode.canceled:
            return
        labels = [self.builder.get_object('total_time_label_{0:d}'.format(i)) for i in range(4)]
        for player, label, color in zip(self.players, labels, COLORS):
            color = color if player.finished else 'black'
            seconds = player.total_seconds
            markup = '<span size="30000" color="{0}">{1:.3f}</span>'.format(
                color, seconds,
            )
            label.set_markup(markup)

        labels = [self.builder.get_object('best_round_label_{0:d}'.format(i)) for i in range(4)]
        for player, label, color in zip(self.players, labels, COLORS):
            color = color if player.finished else 'black'
            try:
                seconds = min(map(lambda x: x.total_seconds(), player.times))
            except ValueError:
                continue
            markup = '<span size="30000" color="{0}">{1:.3f}</span>'.format(
                color, seconds,
            )
            label.set_markup(markup)

        labels = [self.builder.get_object('rank_label_{0:d}'.format(i)) for i in range(4)]
        for player, label, color in zip(self.players, labels, COLORS):
            color = color if player.finished else 'black'
            if not player.rank > 0:
                continue
            markup = '<span size="30000" color="{0}">{1:d}.</span>'.format(
                color, player.rank,
            )
            label.set_markup(markup)

        labels = [self.builder.get_object('rounds_label_{0:d}'.format(i)) for i in range(4)]
        for player, label, color in zip(self.players, labels, COLORS):
            color = color if player.finished else 'black'
            markup = '<span size="30000" color="{0}">{1:d}</span>'.format(
                color, player.rounds,
            )
            label.set_markup(markup)

    def start_time_attack(self):
        """Start a new "time attack" race.

        Works the same like `start_match`, it just uses the gamemode "TimeAttack"

        """
        race_box = self.builder.get_object('race_box')


        self.mode = TimeAttack(self.device, len(self.players), seconds=seconds)
        self.mode.start()

        if not 1 < len(self.players) < 5:
            return
        race_mainbox = self.builder.get_object('race_mainbox')
        self.time_label = time_label = gtk.Label()
        time_label.set_use_markup(True)
        time_label.set_markup('<span size="42000">00:00</span>')
        time_label.show()
        race_mainbox.pack_start(time_label, expand=False)
        race_mainbox.reorder_child(time_label, 0)
        for color, player in zip(COLORS, self.players):
            vbox = gtk.VBox()

            playername = gtk.Label()
            playername.set_use_markup(True)
            playername.set_markup('<span size="18000" color="{0}">{1}</span>'.format(
                color, player
            ))
            vbox.add(playername)
            playername.show()

            round_ = gtk.Label()
            round_.set_use_markup(True)
            round_.set_markup('<span size="36000">1</span>')
            vbox.add(round_)
            round_.show()

            race_box.add(vbox)
            vbox.show()
        boxes = self.builder.get_object('race_box').children()
        last_rounds = [0] * len(self.players)

        last_time_left = timedelta()
        graph = graphs.TimeAttack(len(self.players))
        self.builder.get_object('round_graph').add(graph.canvas)
        graph.show()
        need_draw = True
        while not self.mode.finished:
            while gtk.events_pending():
                gtk.main_iteration()
            self.mode.poll()
            for i, box in enumerate(boxes):
                try:
                    if last_rounds[i] != self.mode.player_rounds[i]:
                        text = '<span size="36000">{0}</span>'.format(
                            self.mode.player_rounds[i] + 1)
                        box.children()[1].set_markup(text)
                        last_rounds[i] = self.mode.player_rounds[i]
                        graph.add(i)
                        need_draw = True
                except IndexError:
                    pass
            if last_time_left == timedelta() or \
               last_time_left - self.mode.time_left > timedelta(seconds=1):
                delta = max(self.mode.time_left, timedelta())
                text = '<span size="42000">{0:02}:{1:02}</span>'.format(
                    *divmod(delta.seconds, 60))
                time_label.set_markup(text)
                last_time_left = delta
            if need_draw:
                graph.draw()
                need_draw = False
        self.finish_race()

    def start_knockout(self):
        """Start a new "knock out" race.

        Works the same like `start_match`, it just uses the gamemode "KnockOut"

        """
        race_box = self.builder.get_object('race_box')

        self.mode = KnockOut(self.device, len(self.players))
        self.mode.start()

        if not 1 < len(self.players) < 5:
            return
        race_mainbox = self.builder.get_object('race_mainbox')
        hbox = gtk.VBox()
        for color, player in zip(COLORS, self.players):

            playername = gtk.Label()
            playername.set_use_markup(True)
            playername.set_markup('<span size="55000" color="{0}">{1}</span>'.format(
                color, player
            ))
            hbox.add(playername)
            playername.show()

        race_box.add(hbox)
        hbox.show()

        box = self.builder.get_object('race_box').children()[0].children()
        player_already_lost = [False] * len(self.players)
        while not self.mode.finished:
            while gtk.events_pending():
                gtk.main_iteration()
            self.mode.poll()
            for i, label in enumerate(box):
                if self.mode.player_lost[i] and not player_already_lost[i]:
                    text = '<span size="55000" color="grey">{0}</span>'.format(
                        self.players[i])
                    label.set_markup(text)
                    player_already_lost[i] = True
        self.finish_race()

    def start_training(self):
        """Start a "training".

        Makes it possible to use every track independently, driving
        n rounds and then shuts down the track.

        """
        rounds = int(self.button_rounds_num.get_value())
        self.mode = Training(self.device, 4, rounds)
        self.mode.start()
        while not self.mode.finished:
            while gtk.events_pending():
                gtk.main_iteration()
            self.mode.poll()
        self.lock_settings(False)

if __name__ == '__main__':
    carrera = Carrera()
    carrera.run()
