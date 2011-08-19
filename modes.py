"""Contains different game modes."""
from datetime import datetime, timedelta

from devices import UE9

class Mode(object):
    """Baseclass for all modes."""

    def __init__(self):
        self.device = UE9()
        self.finished = False

    def run(self, player_num=2):
        """Method to start the race. Returns when the race is finished."""
        self.player_num = player_num

        self.countdown()
        while not self.finished:
            self.check_sensors()
            self.score()
            self.check_conditions()
        self.save()

    def countdown(self):
        """Handle the countdown for the start."""
        # TODO: traffic lights
        self.device.power_on(-1)
        pass

    def save(self):
        """Write the acquired data to the database."""
        pass

    def check_sensors(self):
        self.tracks = self.device.track_state(self.player_num)

    def score(self):
        pass

    def check_conditions(self):
        pass

class Match(Mode):

#    def __init__(self):
#        super(Match, self).__init__(self, player_num)

    def run(self, player_num=2, rounds=10):
        self.rounds = rounds
        self.player_times = []
        for i in range(player_num):
            self.player_times.append([])
        self.last_times = [datetime.now()] * player_num
        super(Match, self).run(player_num)

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

class TimeAttack(Mode):
    pass
