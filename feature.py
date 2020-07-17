#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:50:32 2020

@author: lsx
"""

import pandas as pd
import numpy as np
import hrv

class Feature(object):
    
    def __init__(self, time=None, vals=None, info=None, event=None):
        self.__time = time
        if isinstance(vals, pd.DataFrame):
            self.__vals = vals
        else:
            raise ValueError('Input Type must be valsFrame')
        self.__info = info
        self.__event = pd.DataFrame(event)
        
    @property
    def time(self):
        return self.__time
        
    @property
    def vals(self):
        return self.__vals        

    @property
    def info(self):
        return self.__info       

    @property
    def event(self):
        return self.__event       
        
    def time_func(self):
        time = self.time[int(len(self.time)/2)]
        return time
    
    def vals_func(self):
        feas = dict()
        cols_fea = self.vals.columns
        for col_fea in cols_fea:
            vals = self.vals[col_fea]
            fea = self.vals_stats_func(vals, col_fea)
            feas.update(fea)
        return feas
                       
    def vals_stats_func(self, vals, col):
        dmean   = np.mean(vals)
        dstd    = np.std(vals)
        dmin    = np.min(vals)
        dmax    = np.max(vals)
        dmedian = np.median(vals)
        return dict(zip([col+'_mean',col+'std',col+'min',col+'max',col+'median'],
                        [dmean,dstd,dmin,dmax,dmedian]))
    
    def vals_hrv_func(self, rri):
        rri = hrv.rri.RRi(rri)
        hrv_feas = dict()
        hrv_time = hrv.classical.time_domain(rri)
        hrv_freq = hrv.classical.frequency_domain(rri)
        hrv_feas.update(hrv_time)
        hrv_feas.update(hrv_freq)
        return hrv_feas     
            
    def info_func(self):
        info = pd.DataFrame(self.info)
        return info
        
    def event_func(self):
        gnds = dict()
        cols_event = self.event.columns
        for col_event in cols_event:
            event = self.event[col_event]
            gnd = self.event_max_func(event, col_event)
            gnds.update(gnd)
        return gnds
        
    def event_max_func(self, event, col_event):
        return {col_event: np.max(event)}
        
    def func(self, fea_hrv=True):
        re = dict()
        feas = self.vals_func()
        re.update(feas)
        if fea_hrv is not None:
            hrv_feas = self.vals_hrv_func(self.vals['rri'])
            re.update(hrv_feas)
        if self.info is not None:
            info = self.info_func()
            re.update(info)
        if self.event is not None:
            gnds = self.event_func()
            re.update(gnds)
        return pd.DataFrame(re, index=[0])
        
        
        
        
        
                            
            
            
        
        
         
            
    
    