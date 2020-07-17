#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 20:40:52 2020

@author: lsx
"""

import pandas as pd
import datetime as dt

def mark_event_seizure(time, events, buff=None):
    events = pd.DataFrame(events)
    event_seizure = pd.DataFrame(time)
    event_seizure['event_seizure'] = 0
    event_seizure = event_seizure.set_index('time')
    for idx in range(len(events)):
        event = events.loc[idx, :]
        event_start = event['event_start'] - dt.timedelta(seconds=buff)
        event_end   = event['event_end'] + dt.timedelta(seconds=buff)
        try:
            event_seizure.loc[event_start:event_end, 'event_seizure'] = 1
        except:
            continue
    event_seizure = event_seizure.reset_index(drop=False)
    return event_seizure

#def mark_event_activate(index, events):