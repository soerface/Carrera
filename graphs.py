import matplotlib
matplotlib.use('GtkAgg')
from matplotlib import pyplot
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.figure import Figure

from constants import COLORS

class Graph(object):

    def __init__(self, num_players=2):
        self.num_players = num_players
        self.figure = Figure(facecolor='#f2f1f0')
        self.canvas = FigureCanvas(self.figure)

    def show(self):
        self.canvas.show()

    def draw(self):
        self.figure.canvas.draw()

class Match(Graph):

    def __init__(self, num_players=1, rounds=1):
        super(Match, self).__init__(num_players)
        self.barchart = self.figure.add_subplot(2, 2, 1,)
        self.linechart = self.figure.add_subplot(2, 1, 2,)
        self.barhchart = self.figure.add_subplot(2, 2, 2)
        self.num_bars = [0 for i in range(num_players)]
        self.total_times = [0 for i in range(num_players)]
        self.seconds = [[] for i in range(num_players)]
        self.lines = [self.linechart.plot(0, 0) for i in range(num_players)]
        self.rounds = rounds
        self.height = self.width = 1
        self.update_axis()
        self.player_finished = 0
        #self.canvas.xlabel('Runde')
        #self.canvas.ylabel('Zeit in Sekunden')

        if num_players == 1:
            self.bar_width = 0.8
            self.padding = 0.1
        elif num_players == 2:
            self.bar_width = 0.4
            self.padding = 0.1
        elif num_players == 3:
            self.bar_width = 0.2
            self.padding = 0.2
        elif num_players == 4:
            self.bar_width = 0.2
            self.padding = 0.1


    def add(self, player, time):
        seconds = time.total_seconds()
        self.total_times[player] += seconds
        x = self.padding + player * self.bar_width + self.num_bars[player]
        bar = self.barchart.bar(x, seconds, color=COLORS[player], width=self.bar_width)
        self.num_bars[player] += 1
        self.width = max(self.rounds, self.num_bars[player])
        self.height = max(self.height, seconds)

        self.seconds[player].append(seconds)
        if len(self.seconds[player]) == self.rounds:
            pos = self.padding + self.num_players - 1 - self.player_finished,
            barh = self.barhchart.barh(pos, self.total_times[player],
                                       color=COLORS[player], height=1 - self.padding * 2)
            self.player_finished += 1

        ydata = []
        for i in range(len(self.seconds[player]) + 1):
            ydata.append(sum(self.seconds[player][:i]))
        pyplot.setp(self.lines[player], xdata=range(len(self.seconds[player]) + 1),
                    ydata=ydata, color=COLORS[player])

        self.update_axis()

    def update_axis(self):
        self.barchart.axis([0, self.width, 0, self.height + 1])
        self.barhchart.axis([0, max(self.total_times) + 1, 0, self.num_players])
        height = 1
        for seconds in self.seconds:
            height = max(height, sum(seconds))
        self.linechart.axis([0, self.width, 0, height + 1])

class TimeAttack(Graph):

    def __init__(self, num_players=2):
        super(TimeAttack, self).__init__(num_players)
        self.barchart = self.figure.add_subplot(1, 1, 1)
        self.scores = [1] * num_players
        self.update_axis()

    def add(self, player):
        #x = self.padding + player * self.bar_width + self.num_bars[player]
        x = player + 0.1
        self.scores[player] += 1
        bar = self.barchart.bar(x, self.scores[player], color=COLORS[player], width=0.8)

        self.update_axis()

    def update_axis(self):
        self.barchart.axis([0, self.num_players, 0, max(self.scores)])
