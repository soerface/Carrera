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
        """Called when a car passes the sensor at the line and is not yet finished"""

    def check_conditions(self):
        """Check for winning conditions.

        Overwrite this method in your gamemode to check for certain conditions,
        e.g. timelimits. Called after every sensor polling.

        """

class Match(Mode):

    def configure(self, rounds):
        self.rounds = rounds

    @property
    def total_times(self):
        """Returns the total time in seconds as string."""
        times = []
        for player in self.player_times:
            seconds = str(sum([d.total_seconds() for d in player]))
            times.append(trim_time(seconds))
        return times

    @property
    def best_round(self):
        """Returns a dictionary with the id of the player who made the best round
        and the time"""
        times = []
        for time in self.player_times:
            times.append(min([d.total_seconds() for d in time]))
        best_time = min(times)
        player_id = times.index(best_time)
        return {'time': best_time, 'player_id': player_id}

    def check_conditions(self):
        """Check if a player made all rounds.

        Turns off the track if a player made all his rounds.
        """
        for player in self.players:
            if len(player.times) >= self.rounds and not player.finished:
                player.finished = True
                player.rank = map(lambda x: x.finished, self.players).count(True)
        if all(map(lambda x: x.finished, self.players)):
            self.finished = True

class TimeAttack(Mode):

    def __init__(self, device, player_num=2, seconds=0):
        super(TimeAttack, self).__init__(device, player_num)
        self.seconds = seconds
        self.player_rounds = [0] * player_num
        self.finish_time = datetime.now()

    def run(self):
        super(TimeAttack, self).run()
        self.finish_time = self.start_time + timedelta(seconds=self.seconds)

    def score(self):
        now = datetime.now()
        for i, sensor in enumerate(self.sensors):
            if i >= self.player_num:
                continue
            if sensor:
                # tolerance to not count a round twice or more
                if now - self.last_times[i] < timedelta(seconds=2):
                    continue
                self.player_rounds[i] += 1
                self.last_times[i] = now

    def check_conditions(self):
        """Check if the time is over

        Used to power off the tracks.
        """
        if self.finish_time <= datetime.now():
            self.device.power_off(-1)
            self.finished = True
            self.device.traffic_lights = 3

    @property
    def time_left(self):
        return self.finish_time - datetime.now()

class KnockOut(Mode):

    def __init__(self, device, player_num=2):
        super(KnockOut, self).__init__(device, player_num)
        self.player_lost = [False] * player_num
        self.player_rounds = [0] * player_num

    def score(self):
        now = datetime.now()
        for i, sensor in enumerate(self.sensors):
            if i >= self.player_num:
                continue
            if sensor:
                # tolerance to not count a round twice or more
                if now - self.last_times[i] < timedelta(seconds=2):
                    continue
                # do not count rounds of dead players
                if self.player_lost[i]:
                    continue
                self.player_rounds[i] += 1

                # kill the n00b
                minimum = min(self.player_rounds)
                if self.player_rounds.count(minimum) == 1:
                    player_id = self.player_rounds.index(minimum)
                    self.device.power_off(player_id)
                    self.player_lost[player_id] = True
                    self.player_rounds[player_id] = 4
                if self.player_lost.count(False) == 1:
                    self.finished = True
                self.last_times[i] = now

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
