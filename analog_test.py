#!/usr/bin/env python

from random import random
from time import sleep

from matplotlib import pyplot

from ue9 import UE9

NUM = 1000

d = UE9()
p = pyplot.plot([])
#pyplot.show()
pyplot.axis([0, NUM, 4.97, 5.0])

l = []
for i in range(NUM):
    val = d.feedback(AINMask=1)['AIN0']
    if val < 4.980 or val > 5:
        sleep(0.1)
        continue
    l.append(val)
    pyplot.setp(p, xdata=range(len(l)), ydata=l)
    pyplot.draw()
