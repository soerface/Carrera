"""Contains different game modes."""
from datetime import datetime, timedelta

class Mode(object):
    """Baseclass for all modes."""

    def __init__(self, device, player_num=2):
        if player_num not in [2,3,4]:
            raise ValueError('player_num needs to be 2, 3 or 4')
        self.device = device
        self.finished = self.started = False
        self.canceled = False
        self.player_num = player_num
        self.player_finished = [False] * player_num

    def start(self):
        """Start a new match."""
        self.started = True
        self.running = False
        self.device.power_off(-1)
        self.start_time = datetime.now()

    def cancel(self):
        """Cancel a match."""
        self.finished = True
        self.canceled = True

    def run(self):
        """Countdown is over, start the race!"""
        self.running = True
        self.start_time = datetime.now()
        self.device.power_on(*range(self.player_num))
        self.device.traffic_lights = 4
        self.last_times = [self.start_time] * self.player_num

    def poll(self):
        """Do some "game logic". Needs to be called as often as possible."""

        # test led to debug performance
        #self.device.device.feedback(FIOMask=0b10000000, FIOState=255, FIODir=255)

        if self.running:
            self.read_sensors()
            self.score()
            self.check_conditions()
        else:
            self.countdown()
            if datetime.now() - self.start_time > timedelta(seconds=4):
                self.run()

        # test led to debug performance
        #self.device.device.feedback(FIOMask=0b10000000, FIOState=0, FIODir=255)

    def countdown(self):
        """Handle the countdown for the start."""
        delta = datetime.now() - self.start_time
        self.device.traffic_lights = delta.seconds

    def save(self):
        """Write the acquired data to the database."""
        pass

    def read_sensors(self):
        self.sensors = self.device.sensor_state(self.player_num)

    def score(self):
        pass

    def check_conditions(self):
        pass

class Match(Mode):

    def __init__(self, device, player_num=2, rounds=5):
        super(Match, self).__init__(device, player_num)
        self.rounds = rounds
        self.player_times = []
        for i in range(player_num):
            self.player_times.append([])

    def score(self):
        now = datetime.now()
        for i, sensor in enumerate(self.sensors):
            if i >= self.player_num:
                continue
            if sensor and not self.player_finished[i]:
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
            if all(self.player_finished):
                self.device.traffic_lights = 0
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
