#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 14:11:06 2019

@author: lsx
"""

import pandas as pd
import datetime as dt
import time
from functools import reduce
from pandas.tseries.offsets import Hour, Minute, Second, DateOffset
from pandas.core.arrays.datetimes import DatetimeArray
import numpy as np
#from collections import deque


class TimePoint(dt.datetime):
    ## TODO: add completed notation
    """
    TimePoint 
    """
    def __init__(self, timepoint):
        super(TimePoint, self).__init__(timepoint)
        self.timepoint = timepoint
        self._valid = self._is_valid()
    
    def _ts_to_dt(self):
        """
        Convert UNIX time to datetime
        """
        if isinstance(self.timepoint, int) and self._valid:
            timepoint = dt.datetime.fromtimestamp(self.timepoint)
        else:
            raise ValueError('Invalid Time Point Type')
        return timepoint
           
    def _str_to_dt(self):
        """
        Convert str to datetime
        """
        if isinstance(self.timepoint, str) and self._valid:
            timepoint = time.strftime('%Y-%m-% %H:%M:%S', self.timepoint)
        else:
            raise ValueError('Invalid Time Point Type')
        return timepoint
                        
    def _is_valid(self):
        if isinstance(self.timepoint, dt.datetime):
            return True
        elif isinstance(self.timepoint, int):
            if len(self.timepoint) == 13:
                return True
            else:
                return False
        elif isinstance(self.timepoint, str):
            # TODO: Add str valid rule
            return True
        else:
            return False
    
    def to_timepoint(self):
        self._valid = self._is_valid()
        if not self._valid:
            raise ValueError('Invalid Time Point Type')
        if isinstance(self.timepoint, str):
            self.timepoint = self._str_to_dt()
        if isinstance(self.timepoint, int):
            self.timepoint = self._ts_to_dt()
            
    def to_rollback(self, tm='min'):
        ## TODO: rollback to End tm (completed Notation)
        """
        """
        ## TODO: add other level
        self.to_timepoint()
        self.timepoint = dt.datetime(year=self.timepoint.year,
                                     month=self.timepoint.month,
                                     day=self.timepoint.day,
                                     hour=self.timepoint.hour,
                                     minute=self.timepoint.minute,
                                     second=0)  
        return self.timepoint
        
    def to_rollforword(self, tm='min'):
        ## TODO: rollforword to End tm (completed Notation)
        """
        """
        ## TODO: add other level
        self.to_timepoint()
        self.timepoint = self.timepoint + dt.timedelta(minutes=1)
        self.to_timepoint()        
        return self.timepoint    
        

def rollback_minute(tpoint):
    ## TODO: add more level
    if isinstance(tpoint, dt.datetime):
        tpoint_ = dt.datetime(year=tpoint.year,
                              month=tpoint.month,
                              day=tpoint.day,
                              hour=tpoint.hour,
                              minute=tpoint.minute,
                              second=0)
    else:
        tpoint_ = tpoint
    return tpoint_

def rollforword_minute(tpoint):
    ## TODO: add more level
    if isinstance(tpoint, dt.datetime):
        tpoint_ = dt.datetime(year=tpoint.year,
                              month=tpoint.month,
                              day=tpoint.day,
                              hour=tpoint.hour,
                              minute=tpoint.minute+1,
                              second=0)
    else:
        tpoint_ = tpoint
    return tpoint_
    
    
class SlidingWindow(object):
    
    def __init__(self, window, overlap, min_size, 
                 normalize, closed, label=None):
        self.window = window
        self.overlap = overlap
        self.min_size = min_size
        self.normalize = normalize
        self.closed = closed
        self.label = label
                
    def _get_slice_index(self, start=None, end=None, periods=None, **kwargs):
        """
        Time Array
        """
        if not periods:
            periods = None    
        
        if self.normalize:
            start = rollback_minute(start)
            end = rollforword_minute(end)
        
        freq = round(self.window * (1-self.overlap))
        freq = str(freq) + 's'
        
        # TODO: Here we use datetime array to get every 
        # start points and end points of windows during whole timeline 
        dtarr = DatetimeArray._generate_range(
            start=start, end=end, periods=periods,
            freq=freq, **kwargs) # generate datetime array
        print(dtarr)
        dtarr_start = dtarr[:-1]
        dtarr_end = dtarr_start + Second(self.window)
        
        if self.closed == 'right':
            dtarr_start = dtarr_start - Second(1)
            
        if self.closed == 'left':
            dtarr_end = dtarr_end - Second(1) 
    
        _index = range(len(dtarr_start))            
        dt_index = list(map(lambda i: (dtarr_start[i], dtarr_end[i]), _index))
        return dt_index        
    
    def _to_slice_windows(self, df, slice_index, time_index=True):
        """
            slice_index: [0] start [1] end
        """
        if time_index:
            windows = list(map(lambda idx: df.loc[idx[0]: idx[1], :].reset_index(drop=False), slice_index))
        else:
            windows = list(map(lambda idx: df.loc[idx[0]: idx[1], :], slice_index))
        return windows
        
    def _get_label(df):
        pass
        
        
    def slice_dataframe(self, df, time_index=True):
        """
        """
        def _drop_windows(windows, min_size):
            windows_ = list()
            for window in windows:
                if len(window) >= min_size:
                    windows_.append(window)
            return windows_
                      
        start = df.index[0]
        end = df.index[-1]
        slice_index = self._get_slice_index(start, end)
        windows = self._to_slice_windows(df, slice_index, time_index=time_index)
        windows = _drop_windows(windows, self.min_size)
        self.windows = Window(windows)
        return Window(windows)
        
    def apply(self, func):
        self.window.func = func
        df = self.window.apply()
        return df
        
        
        
class Window(list):

    def __init__(self, windows):
        super(Window, self).__init__(windows)
        """
        array-like
        """
        self.__windows = list(windows)
        self.__func = lambda df: df

    def __len__(self):
        return len(self.__windows)

    def __getitem__(self, position):
        if isinstance(position, (slice, np.ndarray)):
            return Window(self.__windows[position])
        else:
            return self.__windows[position]        

    @property
    def windows(self):
        return self.__windows
    
    @windows.setter
    def windows(self, windows):
        self.__windows = windows
        
    @property
    def func(self):
        return self.__func
    
    @func.setter
    def func(self, func):
        self.__func = func 

    def _validate_win(windows):
        # TODO: add rule
        windows = list(windows)
        return windows
    
    def apply(self, func=None):
        if not func:
            func = self.func
        else:
            func = func
        windows = map(lambda win: func(win), self.windows)
        df = reduce(lambda win1, win2: pd.concat([win1, win2], axis=0), windows)
        df = df.reset_index(drop=True)
        return df
        
