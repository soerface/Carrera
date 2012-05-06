#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from itertools import izip, count
import pickle

import gtk
from jinja2 import Environment, FileSystemLoader
import LabJackPython

from constants import COLORS, GAMEMODES
from devices import UE9, Virtual
from modes import Match, TimeAttack, KnockOut, Training
from misc import Player
from utils import trim_time

class Carrera(object):
    """Class which handles the GTK interface."""

    def __init__(self):
        self.jinja_env = Environment(loader=FileSystemLoader('templates'))
        self.builder = gtk.Builder()
        self.builder.add_from_file('measurement.glade')
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
        self.players = []
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
            with open('preferences.ini', 'rb') as f:
                self.preferences = pickle.load(f)
        except (IOError, EOFError):
            self.preferences = {
                'auto_print': False,
            }
        checkbutton = self.builder.get_object('auto_print_checkbutton')
        checkbutton.set_active(self.preferences['auto_print'])
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass

    def quit(self, *args, **kwargs):
        """Quit the GUI, cancel any running race and save preferences."""
        if hasattr(self, 'mode'):
            self.mode.cancel()
        with open('preferences.ini', 'wb') as f:
            pickle.dump(self.preferences, f)
        self.device.power_off(-1)
        gtk.main_quit()

    def add_player(self):
        """Add a new player box to the player list."""
        self.builder.get_object('start_race').set_sensitive(True)
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

    def draw_page(self, operation, context, page_no):
        """Formats the page for printing."""
        layout = context.create_pango_layout()
        layout.set_markup(self.template)
        cairo_context = context.get_cairo_context()
        cairo_context.show_layout(layout)

    def lock_settings(self, state):
        """(De)activates interface elements like player names"""
        state = False if state else True
        elements = ['add_player', 'start_race', 'preferences_item']
        for element in elements:
            self.builder.get_object(element).set_sensitive(state)
        elements = ['settings_box', 'player_box']
        for element in elements:
            for child in self.builder.get_object(element).children():
                for subchild in child.children():
                    subchild.set_sensitive(state)
        for child in self.builder.get_object('modes_box').children():
            child.set_sensitive(state)
        self.builder.get_object('cancel_race').set_sensitive(not state)

    def generate_print_operation(self):
        print_op = gtk.PrintOperation()
        print_op.set_n_pages(1)
        print_op.connect('draw_page', self.draw_page)
        return print_op

    def on_cancel_race_clicked(self, obj):
        self.mode.cancel()
        self.clear_racewindow()

    def on_simulation_warning_ok_clicked(self, obj):
        self.builder.get_object('simulation_warning').hide()
        self.builder.get_object('race').show()
        self.builder.get_object('main').present()

    def on_auto_print_checkbutton_toggled(self, obj):
        self.preferences['auto_print'] = obj.get_active()

    def on_preferences_item_activate(self, obj):
        self.builder.get_object('preferences').show()

    def on_print_item_activate(self, obj):
        print_op = self.generate_print_operation()
        print_op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, None)

    def on_add_player_clicked(self, obj):
        self.add_player()

    def on_remove_player_clicked(self, obj):
        row = obj.parent
        box = row.parent
        box.remove(row)
        self.builder.get_object('add_player').set_sensitive(True)
        if len(self.player_names) == 0:
            self.builder.get_object('start_race').set_sensitive(False)

    def on_start_race_clicked(self, obj):
        self.clear_racewindow()
        self.lock_settings(True)
        self.players = [Player(i, self.device, name) for i, name in enumerate(self.player_names)]

        if self.gamemode == 'Match':
            rounds = int(self.button_rounds_num.get_value())
            condition = 'Absolviere als erster {0:d} Runden'.format(rounds)
            self.mode = Match(self.device, self, self.players, rounds=rounds)

        elif self.gamemode == 'TimeAttack':
            seconds = int(self.button_seconds.get_value())
            condition = 'Fahre in {0:d} Sekunden soviele Runden wie möglich!'.format(seconds)
            self.mode = TimeAttack(self.device, self, self.players, seconds=seconds)

        elif self.gamemode == 'KnockOut':
            condition = 'Überlebe als letzer'
            self.mode = KnockOut(self.device, self, self.players)

        elif self.gamemode == 'Training':
            rounds = int(self.button_rounds_num.get_value())
            condition = 'Training: {0:d} Runden pro Spur'.format(rounds)
            # use all tracks and no playernames in training mode
            self.players = [Player(i, self.device, '-') for i in range(4)]
            self.mode = Training(self.device, self, self.players, rounds)

        # insert playerdata into racewindow
        names = [x.name for x in self.players]
        for i, color, player_name in izip(count(), COLORS, names):
            label = self.builder.get_object('player_label_{0:d}'.format(i))
            markup = '<span size="30000" color="{0}">{1}</span>'.format(
                color, player_name
            )
            label.set_markup(markup)

        self.builder.get_object('condition_label').set_text(condition)

        self.mode.run()
        if not self.mode.canceled:
            self.prepare_template()
            if self.preferences['auto_print']:
                print_op = self.generate_print_operation()
                print_op.run(gtk.PRINT_OPERATION_ACTION_PRINT, None)
        self.lock_settings(False)

    def on_main_delete_event(self, obj, event):
        self.quit()

    def on_preferences_delete_event(self, obj, event):
        obj.hide()
        return True

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

    def power_on(self, track):
        """Power the given track on. Pass -1 to power all on"""
        self.device.power_on(track)

    def power_off(self, track):
        """Power the given track off. Pass -1 to power all off"""
        self.device.power_off(track)

    on_power_on_0_clicked = lambda self, obj: self.set_power(0, True)
    on_power_off_0_clicked = lambda self, obj: self.set_power(0, False)
    on_power_on_1_clicked = lambda self, obj: self.set_power(1, True)
    on_power_off_1_clicked = lambda self, obj: self.set_power(1, False)
    on_power_on_2_clicked = lambda self, obj: self.set_power(2, True)
    on_power_off_2_clicked = lambda self, obj: self.set_power(2, False)
    on_power_on_3_clicked = lambda self, obj: self.set_power(3, True)
    on_power_off_3_clicked = lambda self, obj: self.set_power(3, False)
    on_power_on_all_clicked = lambda self, obj: self.set_power(-1, True)
    on_power_off_all_clicked = lambda self, obj: self.set_power(-1, False)

    def set_power(self, track, state):
        if state:
            self.device.power_on(track)
        else:
            self.device.power_off(track)
        if track == -1:
            for player in self.players:
                player.banned = not state
                if self.gamemode == 'Training':
                    if player.disabled:
                        self.mode.reset_player(player)
        else:
            try:
                player = self.players[track]
                player.banned = not state
                if self.gamemode == 'Training':
                    if player.disabled:
                        self.mode.reset_player(player)
            except IndexError:
                pass

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

    def prepare_template(self):
        """Renders the print template and unlocks interface."""
        round_times = []
        max_rounds = max(self.players, key=lambda x: x.rounds).rounds
        for i in range(max_rounds):
            round_ = []
            for player in self.players:
                try:
                    seconds = trim_time(player.times[i].total_seconds())
                except IndexError:
                    seconds = '-  '
                round_.append(seconds)
            round_times.append(round_)
        kwargs = {
            'current_date_time': datetime.now().strftime('%d.%m.%Y %H:%M'),
            'players': self.players,
            'total_times': [trim_time(player.total_seconds) for player in self.players],
            'round_times': round_times,
        }
        if self.gamemode == 'Match':
            kwargs['round_num'] = self.mode.rounds
        if self.gamemode == 'TimeAttack':
            kwargs['time_limit'] = self.mode.seconds

        template = self.jinja_env.get_template('{0}.xml'.format(self.gamemode))
        self.template = template.render(**kwargs)
        self.builder.get_object('print_item').set_sensitive(True)
        self.lock_settings(False)

    def update(self):
        """Called by gamemode to update interface"""
        while gtk.events_pending():
            gtk.main_iteration()
        if self.mode.canceled:
            return
        labels = [self.builder.get_object('total_time_label_{0:d}'.format(i)) for i in range(4)]
        colors = []
        for player, color in zip(self.players, COLORS):
            if player.banned:
                colors.append('grey')
            elif player.finished:
                colors.append(color)
            else:
                colors.append('black')

        for player, label, color in zip(self.players, labels, colors):
            seconds = player.total_seconds
            markup = '<span size="30000" color="{0}">{1:.3f}</span>'.format(
                color, seconds,
            )
            label.set_markup(markup)

        labels = [self.builder.get_object('best_round_label_{0:d}'.format(i)) for i in range(4)]
        for player, label, color in zip(self.players, labels, colors):
            seconds = player.best_round
            if seconds is None:
                markup = '<span size="30000" color="{0}">-</span>'.format(
                    color
                )
            else:
                markup = '<span size="30000" color="{0}">{1:.3f}</span>'.format(
                    color, seconds,
                )
            label.set_markup(markup)

        labels = [self.builder.get_object('rank_label_{0:d}'.format(i)) for i in range(4)]
        for player, label, color in zip(self.players, labels, colors):
            if not player.rank > 0:
                continue
            markup = '<span size="30000" color="{0}">{1:d}.</span>'.format(
                color, player.rank,
            )
            label.set_markup(markup)

        labels = [self.builder.get_object('rounds_label_{0:d}'.format(i)) for i in range(4)]
        for player, label, color in zip(self.players, labels, colors):
            markup = '<span size="30000" color="{0}">{1:d}</span>'.format(
                color, player.rounds,
            )
            label.set_markup(markup)

if __name__ == '__main__':
    carrera = Carrera()
    carrera.run()
