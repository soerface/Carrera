from matplotlib import pyplot

COLORS = ['blue', 'red', 'green', 'black']

class Rounds(object):

    def __init__(self):
        self.num_graphs = 0
        self.bars = []
        self.width = self.height = 1
        pyplot.xlabel('Runde')
        pyplot.ylabel('Zeit in Sekunden')

    def add(self, times):
        seconds = [time.total_seconds() for time in times]
        self.bars.append([])
        for i, time in enumerate(seconds):
            bar = pyplot.bar(i + 0.1, time, color=COLORS[len(self.bars) - 1])
            self.bars[-1].append(bar)
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
        #l1 = pyplot.plot(seconds)
        #pyplot.setp(l1, linestyle='steps')
        #x = range(1, len(seconds) + 1)
        #fill = pyplot.fill_between(x, 0, seconds, facecolor=COLORS[self.num_graphs],
        #                           alpha=0.5)
        self.num_graphs += 1
        self.width = max(self.width, len(seconds))
        self.height = max(self.height, *seconds)
        pyplot.axis([0, self.width, 0, self.height])

    def show(self):
        pyplot.show()
