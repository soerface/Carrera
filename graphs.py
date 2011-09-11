import matplotlib
matplotlib.use('GtkAgg')
from matplotlib import pyplot
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.figure import Figure

COLORS = ['blue', 'red', 'green', 'black']

class Rounds(object):

    def __init__(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(1, 2, 1)
        self.num_graphs = 0
        self.bars = []
        self.scores = []
        self.width = self.height = 1
        pyplot.xlabel('Runde')
        pyplot.ylabel('Zeit in Sekunden')

    def add(self, times):
        seconds = [time.total_seconds() for time in times]
        self.bars.append([])
        self.scores.append([])
        for i, time in enumerate(seconds):
            bar = self.ax.bar(0, time, color=COLORS[len(self.bars) - 1])
            score = self.ax.text(0, time + 0.05, '{0:.2f}'.format(time),
                                rotation=90)
            self.bars[-1].append(bar)
            self.scores[-1].append(score)
        if len(self.bars) == 1:
            width = 0.8
            padding = 0.1
        elif len(self.bars) == 2:
            width = 0.4
            padding = 0.1
        elif len(self.bars) == 3:
            width = 0.2
            padding = 0.2
        elif len(self.bars) == 4:
            width = 0.2
            padding = 0.1
        for i, bars in enumerate(self.bars):
            for j, bar in enumerate(bars):
                pyplot.setp(bar, x=(padding + j) + i * width, width=width)
        for i, scores in enumerate(self.scores):
            for j, score in enumerate(scores):
                pyplot.setp(score, x=(padding + j) + i * width + 0.05)
        self.num_graphs += 1
        self.width = max(self.width, len(seconds))
        self.height = max(self.height, *seconds)
        self.ax.axis([0, self.width, 0, self.height + 1])

    def show(self):
        self.canvas.show()
