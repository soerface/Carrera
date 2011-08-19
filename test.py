#!/usr/bin/env python

from datetime import datetime, time, timedelta

from devices import UE9

d = UE9()
times = [[], [], [], []]
now = datetime.now()
last_time = [now] * 4
while True:
    state = d.track_state(4)
    for i, track in enumerate(state):
        if track:
            if datetime.now() - last_time[i] < timedelta(seconds=3):
                continue
            d.enable_power(i)
            times[i].append(datetime.now() - last_time[i])
            last_time[i] = datetime.now()
            print 'Spieler {player}, Runde {round}: {time}'.format(player = i,
                  round = len(times[i]), time=times[i][-1])
