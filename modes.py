"""Contains different game modes."""
from datetime import datetime, timedelta

from devices import UE9

class Mode(object):
    """Baseclass for all modes."""

    def __init__(self, player_num=2):
        if player_num not in [2,3,4]:
            raise ValueError('player_num needs to be 2, 3 or 4')
        self.device = UE9()
        self.finished = self.started = False
        self.player_num = player_num
        self.player_finished = [False] * player_num

    def start(self):
        """Start a new match."""
        self.started = True
        self.running = False
        self.device.power_off(-1)
        self.start_time = datetime.now()

    def _run(self):
        """Countdown is over, start the race!"""
        self.running = True
        self.start_time = datetime.now()
        self.device.power_on(*range(self.player_num))
        self.device.traffic_lights = 4

    def poll(self):
        """Do some "game logic". Needs to be called as often as possible."""

        # test led to debug performance
        self.device.device.feedback(FIOMask=0b10000000, FIOState=255, FIODir=255)

        if self.running:
            self.read_sensors()
            self.score()
            self.check_conditions()
        else:
            self.countdown()
            if datetime.now() - self.start_time > timedelta(seconds=4):
                self._run()

        # test led to debug performance
        self.device.device.feedback(FIOMask=0b10000000, FIOState=0, FIODir=255)

    def countdown(self):
        """Handle the countdown for the start."""
        delta = datetime.now() - self.start_time
        self.device.traffic_lights = delta.seconds

    def save(self):
        """Write the acquired data to the database."""
        pass

    def read_sensors(self):
        self.sensors= self.device.sensor_state(self.player_num)

    def score(self):
        pass

    def check_conditions(self):
        pass

class Match(Mode):

    def __init__(self, player_num=2, rounds=5):
        super(Match, self).__init__(player_num)
        self.rounds = rounds
        self.player_num = player_num
        self.player_times = []
        for i in range(player_num):
            self.player_times.append([])

    def start(self):
        super(Match, self).start()

    def _run(self):
        super(Match, self)._run()
        self.last_times = [self.start_time] * self.player_num

    def score(self):
        for i, sensor in enumerate(self.sensors):
            if sensor and not self.player_finished[i]:
                now = datetime.now()
                # tolerance to not count a round twice or more
                if now - self.last_times[i] < timedelta(seconds=2):
                    continue

                self.player_times[i].append(now - self.last_times[i])
                self.last_times[i] = now


    def check_conditions(self):
        now = datetime.now()
        for i, times in enumerate(self.player_times):
            if len(times) == self.rounds and not self.player_finished[i]:
                self.device.power_off(i)
                self.player_finished[i] = True
                self.device.traffic_lights = 3
            if any(self.player_finished) and now - self.last_times[i] < timedelta(seconds=1):
                self.device.power_off(i)
                self.player_finished[i] = True
            if all(self.player_finished):
                self.device.traffic_lights = 0
                self.finished = True

class TimeAttack(Mode):
    pass
