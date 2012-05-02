#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

class Player(object):

    def __init__(self, track, device, name):
        self.track = track
        self.device = device
        self.name = name
        self.times = []
        self.finished = False
        self.banned = False
        self.total_time = timedelta(seconds=0)
        self.rank = 0

    @property
    def rounds(self):
        return len(self.times)

    @property
    def best_round(self):
        try:
            return min(map(lambda x: x.total_seconds(), self.times))
        except ValueError:
            return None

    @property
    def total_seconds(self):
        return self.total_time.total_seconds()

    @property
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, value):
        self._finished = value
        if value:
            self.device.power_off(self.track)

    @property
    def banned(self):
        return self._banned

    @banned.setter
    def banned(self, value):
        self._banned = value
        if value:
            self.device.power_off(self.track)

    @property
    def disabled(self):
        return self.finished or self.banned
