#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module contains the devices to communicate with the track."""

from datetime import datetime, timedelta
from random import random, shuffle

import ue9

class UE9(ue9.UE9):

    def __init__(self, *args, **kwargs):
        super(UE9, self).__init__(*args, **kwargs)
        self.feedback(EIOMask=255, EIOState=0, EIODir=0b11110000)
        self.traffic_lights = 3
        self.computer_speed = 0

    def _power(self, state, tracks):
        """Set the power for the given tracks accordingly to the passed state.

        All other tracks will not be affected.

        Track | Port
        0     | EIO4
        1     | EIO5
        2     | EIO6
        3     | EIO7

        """
        if len(tracks) == 1 and tracks[0] == -1:
            mask = 255
        else:
            mask = 0
            for track in tracks:
                mask |= 1 << (track + 4)
        self.feedback(EIOMask=mask, EIOState=state, EIODir=0b11110000)

    def power_on(self, *tracks):
        """Enables the power for the given tracks. Pass -1 to enable all."""
        self._power(240, tracks)

    def power_off(self, *tracks):
        """Disables the power for the given tracks. Pass -1 to disable all."""
        self._power(0, tracks)

    @property
    def traffic_lights(self):
        """Set the state of the traffic lights.

        * 0 = 0 red, 0 green
        * 1 = 1 red, 0 green
        * 2 = 2 red, 0 green
        * 3 = 3 red, 0 green
        * 4 = 0 red, 1 green

        Uses ports FIO0 - FIO4

        """
        return self._traffic_lights

    @traffic_lights.setter
    def traffic_lights(self, value):
        if 0 <= value < 4:
            state = 2 ** value - 1
        elif value == 4:
            state = 0b1000
        else:
            raise ValueError('Value must be in range 0-4')
        self._traffic_lights = value
        self.feedback(FIOMask=0b1111, FIOState=state, FIODir=0b1111)

    @property
    def computer_speed(self):
        """Deprecated. Selfdriving car is now controlled via the Arduino."""
        return self._computer_speed

    @computer_speed.setter
    def computer_speed(self, value):
        #TODO: enable and disabled DAC0 in a separate function
        if 0 > value > 4095:
            raise ValueError('Value must be between 0 and 4095')
        self.feedback(DAC0Update=True, DAC0=int(value), DAC0Enabled=True)

    def sensor_state(self):
        """Returns the state of the sensors at the finish line.

        The state is returned as a list with four booleans, one for each
        sensor. It uses the ports EIO0 - EIO3.

        """
        state = self.feedback()['EIOState']
        return [not state & 0b1, not state & 0b10,
                not state & 0b100, not state & 0b1000]

class Virtual(object):
    """Virtual device for testing purposes."""

    def __init__(self):
        self.traffic_lights = 3
        self.last_sensor_return = datetime.now()

    def power_on(self, *tracks):
        """Enables the power for the given tracks. Pass -1 to enable all."""
        print 'power on: {0}'.format(tracks)

    def power_off(self, *tracks):
        """Disables the power for the given tracks. Pass -1 to disable all."""
        print 'power off: {0}'.format(tracks)

    @property
    def traffic_lights(self):
        """Set the state of the traffic lights.

        * 0 = 0 red, 0 green
        * 1 = 1 red, 0 green
        * 2 = 2 red, 0 green
        * 3 = 3 red, 0 green
        * 4 = 0 red, 1 green

        """
        return self._traffic_lights

    @traffic_lights.setter
    def traffic_lights(self, value):
        if value not in range(5):
            raise ValueError('Value must be in range 0-4')
        self._traffic_lights = value
        print 'Traffic lights: {0:d}'.format(value)

    def sensor_state(self):
        """Returns the state of the sensors at the finish line.

        The state is returned as a list with four booleans, one for each
        sensor. It "activates" the sensors randomly.

        """
        now = datetime.now()
        if now - self.last_sensor_return > timedelta(seconds=1+10*random()):
            self.last_sensor_return = now
            l = [True, False, False, False]
            shuffle(l)
            return l
        return [False, False, False, False]
