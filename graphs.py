import matplotlib
matplotlib.use('GtkAgg')
from matplotlib import pyplot
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.figure import Figure

COLORS = ['blue', 'red', 'green', 'black']

class Rounds(object):

    def __init__(self, num_graphs=1, width=1):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(1, 1, 1, label='blub')
        self.bars = [[] for i in range(num_graphs)]
        self.scores = [[] for i in range(num_graphs)]
        self.width = width
        self.height = 1
        self.ax.axis([0, self.width, 0, self.height + 1])
        #self.canvas.xlabel('Runde')
        #self.canvas.ylabel('Zeit in Sekunden')

        if num_graphs == 1:
            self.bar_width = 0.8
            self.padding = 0.1
        elif num_graphs == 2:
            self.bar_width = 0.4
            self.padding = 0.1
        elif num_graphs == 3:
            self.bar_width = 0.2
            self.padding = 0.2
        elif num_graphs == 4:
            self.bar_width = 0.2
            self.padding = 0.1


    def add(self, player, time):
        seconds = time.total_seconds()
        x = self.padding + player * self.bar_width + len(self.bars[player])
        bar = self.ax.bar(x, seconds, color=COLORS[player], width=self.bar_width)
        score = self.ax.text(x + 0.1, seconds + 0.05, '{0:.2f}'.format(seconds),
                            rotation=90)
        self.bars[player].append(bar)
        self.scores[player].append(score)
        self.width = max(self.width, len(self.bars[player]))
        self.height = max(self.height, seconds)
        self.ax.axis([0, self.width, 0, self.height + 1])
        self.draw()

    def show(self):
        self.canvas.show()

    def draw(self):
        self.figure.canvas.draw()
