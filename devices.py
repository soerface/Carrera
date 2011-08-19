"""This module contains the devices to communicate with the track."""

import ue9

class UE9(object):

    def __init__(self):
        self.device = ue9.UE9()

    @property
    def player(self, num):
        pass

    #def traffic_light(self):
    #    pass

    def track_state(self, num):
        feedback = self.device.feedback(EIOMask=255, EIODir=0)
        state = feedback['EIOState']
        return [not state & 0b1, not state & 0b10,
                not state & 0b100, not state & 0b1000]
