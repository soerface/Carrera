import matplotlib
matplotlib.use('GtkAgg')
from matplotlib import pyplot
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.figure import Figure

COLORS = ['blue', 'red', 'green', 'black']

class Graph(object):

    def __init__(self, num_graphs=1, width=1):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.barchart = self.figure.add_subplot(2, 1, 1,)
        self.linechart = self.figure.add_subplot(2, 1, 2,)
        self.num_bars = [0 for i in range(num_graphs)]
        self.seconds = [[] for i in range(num_graphs)]
        self.lines = [self.linechart.plot(0, 0) for i in range(num_graphs)]
        self.width = width
        self.height = 1
        self.update_axis()
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
        x = self.padding + player * self.bar_width + self.num_bars[player]
        bar = self.barchart.bar(x, seconds, color=COLORS[player], width=self.bar_width)
        self.num_bars[player] += 1
        self.width = max(self.width, self.num_bars[player])
        self.height = max(self.height, seconds)
        self.update_axis()

        self.seconds[player].append(seconds)
        ydata = []
        for i in range(len(self.seconds[player]) + 1):
            ydata.append(sum(self.seconds[player][:i]))
        pyplot.setp(self.lines[player], xdata=range(len(self.seconds[player]) + 1),
                    ydata=ydata, color=COLORS[player])

    def show(self):
        self.canvas.show()

    def draw(self):
        self.figure.canvas.draw()

    def update_axis(self):
        self.barchart.axis([0, self.width, 0, self.height + 1])
        height = 1
        for seconds in self.seconds:
            height = max(height, sum(seconds))
        self.linechart.axis([0, self.width, 0, height + 1])
