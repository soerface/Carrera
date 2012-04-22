#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import gtk
from jinja2 import Environment, FileSystemLoader
import LabJackPython

from constants import COLORS
from devices import UE9, Virtual
import graphs
from modes import Match, TimeAttack, KnockOut

GAMEMODES = ['Match', 'TimeAttack', 'KnockOut']

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
        if hasattr(self, 'match'):
            self.match.cancel()
        gtk.main_quit()

    def add_player(self):
        """Add a new player box to the player list."""
        if len(self.players) == 4:
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

        layout = context.create_pango_layout()
        if self.last_gamemode == 'Match':
            template = self.jinja_env.get_template('match')
            best_round = {
                'time': self.match.best_round['time'],
                'player': self.last_players[self.match.best_round['player_id']],
            }
            layout.set_markup(template.render(
                players = self.last_players,
                total_times = self.match.total_times,
                worst_time = max(self.match.total_times),
                current_time = datetime.now().strftime('%d.%m.%Y %H:%M'),
                best_round = best_round,
                round_num = self.match.rounds,
                round_times = self.match.round_times,
                )
            )
        cairo_context = context.get_cairo_context()
        cairo_context.show_layout(layout)

    def lock_settings(self, state):
        """(De)activates interface elements like player names"""
        state = False if state else True
        for element in ['add_player', 'start_race']:
            self.builder.get_object(element).set_sensitive(state)
        for element in ['settings_box', 'player_box']:
            for child in self.builder.get_object(element).children():
                for subchild in child.children():
                    subchild.set_sensitive(state)
        for child in self.builder.get_object('modes_box').children():
            child.set_sensitive(state)

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

    def on_start_race_clicked(self, obj):
        self.clear_racewindow()
        self.builder.get_object('print_item').set_sensitive(False)
        self.lock_settings(True)
        if self.gamemode == 'Match':
            self.start_match()
        elif self.gamemode == 'TimeAttack':
            self.start_time_attack()
        elif self.gamemode == 'KnockOut':
            self.start_knockout()

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
        if hasattr(self, 'match'):
            self.match.cancel()
        for box in self.builder.get_object('race_box').children():
            self.builder.get_object('race_box').remove(box)
        if hasattr(self, 'time_label'):
            self.builder.get_object('race_mainbox').remove(self.time_label)
        try:
            canvas = self.builder.get_object('round_graph').children()[0]
            self.builder.get_object('round_graph').remove(canvas)
        except IndexError:
            pass

    @property
    def players(self):
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
        self.last_players = self.players
        self.builder.get_object('print_item').set_sensitive(True)
        self.lock_settings(False)

    def start_match(self):
        """Start a new "match" race.

        Fetches information from the main window to prepare the racewindow.
        It then goes in an infinite loop to poll the sensors. After all players
        finished the loop will be interrupted.

        """
        race_box = self.builder.get_object('race_box')
        if not 1 < len(self.players) < 5:
            return
        rounds = int(self.button_rounds_num.get_value())
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
            round_.set_markup('<span size="36000">1/{0}</span>'.format(rounds))
            vbox.add(round_)
            round_.show()

            race_box.add(vbox)
            vbox.show()
        self.match = Match(self.device, len(self.players), rounds=rounds)
        self.match.start()
        boxes = self.builder.get_object('race_box').children()
        last_times = [None] * len(self.players)

        graph = graphs.Match(len(self.players), rounds=rounds)
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
        self.finish_race()

    def start_time_attack(self):
        """Start a new "time attack" race.

        Works the same like `start_match`, it just uses the gamemode "TimeAttack"

        """
        race_box = self.builder.get_object('race_box')

        seconds = int(self.button_seconds.get_value())

        self.match = TimeAttack(self.device, len(self.players), seconds=seconds)
        self.match.start()

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
        while not self.match.finished:
            while gtk.events_pending():
                gtk.main_iteration()
            self.match.poll()
            for i, box in enumerate(boxes):
                try:
                    if last_rounds[i] != self.match.player_rounds[i]:
                        text = '<span size="36000">{0}</span>'.format(
                            self.match.player_rounds[i] + 1)
                        box.children()[1].set_markup(text)
                        last_rounds[i] = self.match.player_rounds[i]
                        graph.add(i)
                        need_draw = True
                except IndexError:
                    pass
            if last_time_left == timedelta() or \
               last_time_left - self.match.time_left > timedelta(seconds=1):
                delta = max(self.match.time_left, timedelta())
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

        self.match = KnockOut(self.device, len(self.players))
        self.match.start()

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
        while not self.match.finished:
            while gtk.events_pending():
                gtk.main_iteration()
            self.match.poll()
            for i, label in enumerate(box):
                if self.match.player_lost[i] and not player_already_lost[i]:
                    text = '<span size="55000" color="grey">{0}</span>'.format(
                        self.players[i])
                    label.set_markup(text)
                    player_already_lost[i] = True
        self.finish_race()

if __name__ == '__main__':
    carrera = Carrera()
    carrera.run()
