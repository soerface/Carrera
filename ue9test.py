#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep

from ue9 import UE9

dev = UE9()
# clear
dev.feedback(EIOMask=255, EIOState=0, EIODir=255,
             FIOMask=255, FIOState=0, FIODir=255)
sleep(1)
result = 2**16
i = 0
while True:

    if i / 8 == 1:
        dev.feedback(EIOMask=255, EIOState=2**(i % 8)|(result >> 8), EIODir=255)
        dev.feedback(FIOMask=255, FIOState=result, FIODir=255)
    else:
        dev.feedback(EIOMask=255, EIOState=result >> 8, EIODir=255)
        dev.feedback(FIOMask=255, FIOState=2**(i % 8)|result, FIODir=255)
    i += 1
    if (result >> i) & 1:
        result |= 2**(i-1)
        i = 0
    if result == 2 ** 17 - 1:
        break
    sleep(0.05)

for i in range(99):
    dev.feedback(EIOMask=255, EIOState=0 if i % 3 else 255, EIODir=255,
                 FIOMask=255, FIOState=0 if i % 3 else 255, FIODir=255)
    sleep(1.0 / (i+1))

i = 0
direction = 'left'
while True:

    if i / 8 == 1:
        dev.feedback(EIOMask=255, EIOState=1 << i >> 8, EIODir=255)
        dev.feedback(FIOMask=255, FIOState=0, FIODir=255)
    else:
        dev.feedback(EIOMask=255, EIOState=0, EIODir=255)
        dev.feedback(FIOMask=255, FIOState=1 << i, FIODir=255)
    if direction == 'left':
        i += 1
        if i == 15:
            direction = 'right'
    elif direction == 'right':
        i -= 1
        if i == 0:
            direction = 'left'
    sleep(0.05)
