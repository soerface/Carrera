#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains different game modes."""
from datetime import datetime, timedelta

from utils import trim_time

class Mode(object):
    """Baseclass for all modes."""

    def __init__(self, device, ui, players, *args, **kwargs):
        if len(players) not in [2, 3, 4]:
            raise ValueError('You need to pass 2, 3 or 4 players in a list')
        self.device = device
        self.ui = ui
        self.finished = False
        self.canceled = False
        self.players = players
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        """Make further configurations.

        Overwrite this method if you want to use more arguments.
        Additional arguments to __init__ will be passed to this method after
        the other arguments (device, ui, players) have been processed.

        """

    def cancel(self):
        """Cancel a match."""
        self.finished = True
        self.canceled = True

    def run(self):
        """Give control to the gamemode until the race is finished."""
        self.finished = False
        self.device.power_off(-1)
        self.start_time = datetime.now()
        countdown = True
        while not self.finished:
            now = self.now = datetime.now()
            delta = datetime.now() - self.start_time
            if countdown:
                self.device.traffic_lights = delta.seconds
                if delta > timedelta(seconds=4):
                    countdown = False
                    self.start_time = datetime.now()
                    self.device.traffic_lights = 4
                    for player in self.players:
                        player.last_time = player.last_pass = now
                    self.device.power_on(*map(lambda x: x.track, self.players))
                self.ui.update()
                continue
            sensor_state = self.device.sensor_state()
            for sensor, player in zip(sensor_state, self.players):
                if sensor:
                    if not player.finished and now - player.last_pass > timedelta(seconds=1):
                        self._on_player_passed_line(player)
                        player.last_time = now
                    player.last_pass = now
                if not player.finished:
                    player.total_time = now - self.start_time
            self.check_conditions()
            self.ui.update()

    def save(self):
        """Write the acquired data to the database."""

    def _on_player_passed_line(self, player):
        player.times.append(self.now - player.last_time)
        self.on_player_passed_line(player)

    def on_player_passed_line(self, player):
        """Called when a car passes the sensor at the line and is not yet finished.

        Round time will be saved before calling and is accessable via the
        player object.

        """

    def check_conditions(self):
        """Check for winning conditions.

        Overwrite this method in your gamemode to check for certain conditions,
        e.g. timelimits. Called after every sensor polling.

        """

    @property
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, value):
        self._finished = value
        if value == True:
            self.device.power_off(-1)
            for player in self.players:
                player.finished = True

class Match(Mode):

    def configure(self, rounds):
        self.rounds = rounds

    def on_player_passed_line(self, player):
        if len(player.times) >= self.rounds:
            player.finished = True
            player.rank = len([x for x in self.players if x.finished])
        if player.rank == len(self.players):
            self.finished = True

class TimeAttack(Mode):

    def configure(self, seconds):
        self.seconds = seconds

    def check_conditions(self):
        """Check if the time is over

        Used to power off the tracks.

        """
        if self.now - self.start_time >= timedelta(seconds=self.seconds):
            self.finished = True

    def on_player_passed_line(self, player):
        prev_rank = player.rank
        prev_rounds = player.rounds - 1
        rank = len(self.players)
        for p in self.players:
            if p.rounds < player.rounds:
                rank -= 1
        player.rank = rank
        for p in self.players:
            if p.rank == 0:
                continue
            if p.rounds == prev_rounds and p.rank < prev_rank:
                p.rank += 1

class KnockOut(Mode):

    def configure(self):
        pass

    def on_player_passed_line(self, player):
        n = 0
        for p in self.players:
            if p.rounds >= player.rounds:
                n += 1
        if player.rounds + n == len(self.players):
            rank = 4
            if n == 1:
                player.rank = 1
                player.finished = True
            for p in sorted(self.players, key=lambda x: x.rounds):
                if p.rounds < player.rounds:
                    p.rank = rank
                    p.finished = True
                rank -= 1

        if len([x for x in self.players if not x.finished]) == 0:
            self.finished = True

class Training(Mode):

    def __init__(self, device, player_num, rounds=10):
        super(Training, self).__init__(device, player_num)
        self.rounds = rounds
        self.player_rounds = [0] * player_num
        self.player_finished = [False] * player_num

    def score(self):
        now = datetime.now()
        for i, sensor in enumerate(self.sensors):
            if i >= self.player_num or self.player_finished[i]:
                continue
            if sensor:
                if now - self.last_times[i] < timedelta(seconds=2):
                    continue
                self.player_rounds[i] += 1
                self.last_times[i] = now
                print i, self.player_rounds[i]

    def check_conditions(self):
        for i, rounds in enumerate(self.player_rounds):
            if rounds >= self.rounds and not self.player_finished[i]:
                self.device.power_off(i)
                self.player_finished[i] = True
                #self.player_rounds[i] = 0
