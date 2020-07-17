#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 11:48:57 2019

@author: lsx
"""

import pandas as pd
import numpy as np
from functools import reduce
import datetime as dt
import epdbio
import bdata
    
class Patient(object):

    def __init__(self, name, stypes=['ac','gs','hr']):
        self.name = name
        self.stypes = stypes
        self.db = epdbio.DataBase().connect()

#    @property
#    def db(self):
#        return self.__db       

    @property
    def info(self):
        return self._queryInfo()
                
    @property
    def sex(self):
        return self._queryInfo(item='sex')
        
    @property
    def age(self):
        return self._queryInfo(item='age')
    
    @property
    def data(self):
        return self._queryData(self.stypes)
        
    @property
    def event(self):
        return self._queryEvent()

    def _queryInfo(self, item=None):
        info = self.db.load_info(self.name)
        if not item:
            return info
        else:
            info_item = info[item]
            info_item = list(info_item)[0]
            return info_item
    
    def _queryData(self, stypes):
        data = self.db.load_bdata(self.name, stypes)
        return data
        
    def _queryEvent(self):
        try:
            event = self.db.load_event(self.name)
        except:
            event = pd.DataFrame(columns=['event_start', 'event_end'])
        return event
    
    def _mark_event(self, data):
        data = data.set_index('time')
        data['seizure'] = 0
        for event_ in self.event:
            event_start_ = event_['event_start']
            event_end_   = event_['event_end']
            try:
                data.loc[event_start_:event_end_, 'seizure'] = 1
            except:
                continue
        data = data.reset_index(drop=False)
        return data           
        
    def load_dataframe(self, stype=['ac','gs','hr'], event=False, info=False):
        datas = list(self.data.values())
        datas = bdata.alignment_sdata(datas)
        if event:
            datas = self.mark_event(datas)
        if info:
            datas['name'] = self.name
            datas['sex']  = self.sex
            datas['age']  = self.age
        return datas
        
    

#def _select_time(data, data_time):
#    '''
#    '''
#    if isinstance(data_time, list):
#        time_start = data_time[0]
#        time_end   = data_time[1]
#    data_select = data[time_start:time_end]
#    if isinstance(data_time, dt.datetime):
#        time_point = data_time
#    data_select = data[time_point]
#    return data_select
    
    
#def _reform(data):
#    '''
#        _reform implement ...
#    '''
#    if isinstance(data, pd.DataFrame):
#        data = pd.DataFrame(data)
#    data_time = data['time']
#    data_type = data['type']
#    data_vals = data['vals']
#    


       