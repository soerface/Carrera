"""This module contains the devices to communicate with the track."""

from random import random

import ue9

class UE9(ue9.UE9):

    def __init__(self, *args, **kwargs):
        super(UE9, self).__init__(*args, **kwargs)
        self.feedback(EIOMask=255, EIOState=0, EIODir=0b11110000)
        self.traffic_lights = 3

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
        return self._traffic_lights

    @traffic_lights.setter
    def traffic_lights(self, value):
        """Set the state of the traffic lights.

        0 = 0 red, 0 green
        1 = 1 red, 0 green
        2 = 2 red, 0 green
        3 = 3 red, 0 green
        4 = 0 red, 1 green

        """
        if 0 <= value < 4:
            state = 2 ** value - 1
        elif value == 4:
            state = 0b1000
        else:
            raise ValueError('Value must be in range 0-4')
        self._traffic_lights = value
        self.feedback(FIOMask=0b1111, FIOState=state, FIODir=0b1111)

    def sensor_state(self, num):
        state = self.feedback()['EIOState']
        return [not state & 0b1, not state & 0b10,
                not state & 0b100, not state & 0b1000]

class Virtual(object):
    """Virtual device for testing purposes."""

    def __init__(self):
        self.traffic_lights = 3

    def power_on(self, *tracks):
        """Enables the power for the given tracks. Pass -1 to enable all."""
        pass

    def power_off(self, *tracks):
        """Disables the power for the given tracks. Pass -1 to disable all."""
        pass

    @property
    def traffic_lights(self):
        return self._traffic_lights

    @traffic_lights.setter
    def traffic_lights(self, value):
        """Set the state of the traffic lights.

        0 = 0 red, 0 green
        1 = 1 red, 0 green
        2 = 2 red, 0 green
        3 = 3 red, 0 green
        4 = 0 red, 1 green

        """
        if value not in range(5):
            raise ValueError('Value must be in range 0-4')
        self._traffic_lights = value

    def sensor_state(self, num):
        v = random()
        return [
            0 <= v < 0.000025,
            0.000025 <= v < 0.00005,
            0.00005 <= v < 0.000075,
            0.000075 <= v < 0.0001,
        ]
