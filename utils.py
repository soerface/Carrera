#!/usr/bin/env python
# -*- coding: utf-8 -*-

def trim_time(time):
    """Rounds the time to 3 digits after the comma and returns it as a string"""
    return '{0:.3f}'.format(time)
