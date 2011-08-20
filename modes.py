"""Contains different game modes."""
from datetime import datetime, timedelta

from devices import UE9

class Mode(object):
    """Baseclass for all modes."""

    def __init__(self, player_num=2):
        self.device = UE9()
        self.finished = self.started = False
        self.player_num = player_num

    def start(self):
        """Start a new match."""
        self.started = True
        self.running = False
        self.device.power_off(-1)
        self.start_time = datetime.now()

    def poll(self):
        """Do some "game logic". Needs to be called as often as possible."""

        # test led to debug performance
        self.device.device.feedback(FIOMask=0b10000000, FIOState=255, FIODir=255)
        testtime = datetime.now()

        if self.running:
            self.read_sensors()
            self.score()
            self.check_conditions()
        else:
            self.countdown()
            if datetime.now() - self.start_time > timedelta(seconds=4):
                self.running = True
                self.start_time = datetime.now()
                self.device.power_on(-1)
                self.device.traffic_lights = 4

        # test led to debug performance
        self.device.device.feedback(FIOMask=0b10000000, FIOState=0, FIODir=255)

        endtesttime = datetime.now()
        delta = endtesttime - testtime
        print 'Time needed for polling: {0} seconds, {1} microseconds'.format(
            delta.seconds, delta.microseconds)

    def countdown(self):
        """Handle the countdown for the start."""
        delta = datetime.now() - self.start_time
        self.device.traffic_lights = delta.seconds

    def save(self):
        """Write the acquired data to the database."""
        pass

    def read_sensors(self):
        self.tracks = self.device.track_state(self.player_num)

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
        self.last_times = [self.start_time] * self.player_num

    def score(self):
        for i, track in enumerate(self.tracks):
            if track:
                # tolerance to not count a round twice or more
                now = datetime.now()
                if now - self.last_times[i] < timedelta(seconds=2):
                    continue
                self.player_times[i].append(now - self.last_times[i])
                self.last_times[i] = now
                print 'Spieler {player}, Runde {round}: {time}'.format(
                      player = i + 1,
                      round = len(self.player_times[i]),
                      time=self.player_times[i][-1]
                )


    def check_conditions(self):
        for i, times in enumerate(self.player_times):
            if len(times) == self.rounds:
                self.device.power_off(i)
                print ' -------- {0} -------- '.format(sum(times, timedelta()))

class TimeAttack(Mode):
    pass
