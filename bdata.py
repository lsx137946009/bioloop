#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version: 20200417
@author: Sixing Liu, Yaru Chen
"""

import pandas as pd
import numpy as np
import hrv
from functools import reduce
from pandas.core.indexes.datetimes import DatetimeIndex
from utils_math import *


class BaseBData(object):
    
    def __init__(self, data):        
        self.__time_name = None
        self.__vals_name = None
        self.__data = data
                   
    def __len__(self):
        return len(self.__data)

    def __getitem__(self, position):
        ## DOTO: fix att
        if isinstance(position, (slice, np.ndarray)):
            return BaseBData(self.__data[position])
        else:
            return self.__data[position]

    def _construct(self):
        data_time = pd.DataFrame(self.time, columns=self.time_name)
        data_vals = pd.DataFrame(self.vals, columns=self.vals_name)
        data = pd.concat([data_time, data_vals], axis=1)
        return data
        
               
class BDataThreeAxis(BaseBData):
    
    def __init__(self, data):
        super(BDataThreeAxis, self).__init__(data)
        self.__time_name = 'time'
        self.__vals_name = ['ac1','ac2','ac3']
        if isinstance(data, pd.DataFrame):
            self.__data = data
            self.__time = self.data[self.time_name]
            self.__vals = self.data[self.vals_name]            
        elif isinstance(data, list):
            self.__time = data[0]
            self.__vals = data[1]
            self.__data = self._construct()
        else:
            raise ValueError('Input type error: must be dataframe or list')

    def __getitem__(self, position):
        if isinstance(position, (slice, np.ndarray)):
            return BDataThreeAxis(self.__data[position])
        else:
            return self.__data[position]

    @property
    def time_name(self):
        return self.__time_name
    
    @time_name.setter
    def time_name(self, time_name):
        if not isinstance(time_name, str):
            raise ValueError('Column Name should be str')
        self.__time_name = time_name    

    @property
    def vals_name(self):
        return self.__vals_name
        
    @vals_name.setter
    def vals_name(self, vals_name):
        if not (isinstance(vals_name, list) and (len(vals_name)==3)):
            raise ValueError('vals_name should be a list with length 3')
        self.__vals_name = vals_name         

    @property
    def vals(self):
        return self.__vals
        
    @property
    def time(self):
        return self.__time
        
    @property
    def data(self):
        return self.__data
                   
    def modulus(self, add_col=False, col_name='mod'):
        xyz = np.mat(self.vals)
        mod = np.linalg.norm(xyz, ord=2, axis=1, keepdims=True)
        self.mod = mod
        if not add_col:
            return mod
        else:
            self.data[col_name] = mod
            return self.data
            
    def mark_event_activate(self, threshold=1.01, mod=None, 
                      add_col=False, col_name='event_activate'):
        if not mod:
            mod = self.modulus()
        mode = compute_mode(mod)
        threshold = mode * threshold
        ## TODO: running speed up
        mapfunc = np.vectorize(lambda x: 1 if x>=threshold else 0)
        activate = mapfunc(mod)
#        activate = list(map(lambda x: 1 if x>=threshold else 0, mod))
        if not add_col:
            return activate
        else:
            self.data[col_name] = activate
            return self.data
        
            
class BDataHeartRate(BaseBData):
    
    def __init__(self, data=None, vals=None, time=None):
        super(BDataHeartRate, self).__init__(data)
        self.__time_name = 'time'
        self.__vals_name = 'hr'
        if isinstance(data, pd.DataFrame):
            self.__data = data
            self.__time = self.data[self.time_name]
            self.__vals = self.data[self.vals_name]            
        elif isinstance(data, list):
            self.__time = data[0]
            self.__vals = data[1]
            self.__data = self._construct()
        else:
            raise ValueError('Input type error: must be dataframe or list')


    def __len__(self):
        return len(self.__data)

    def __getitem__(self, position):
        if isinstance(position, (slice, np.ndarray)):
            return BDataHeartRate(self.__data[position], self.time[position])
        else:
            return self.__data[position]
        
    @property
    def time_name(self):
        return self.__time_name
    
    @time_name.setter
    def time_name(self, time_name):
        if not isinstance(time_name, str):
            raise ValueError('Column Name should be str')
        self.__time_name = time_name    

    @property
    def vals_name(self):
        return self.__vals_name
        
    @vals_name.setter
    def vals_name(self, vals_name):
        if not isinstance(vals_name, str):
            raise ValueError('Column Name should be str')
        self.__vals_name = vals_name         

    @property
    def vals(self):
        return self.__vals
        
    @property
    def time(self):
        return self.__time
        
    @property
    def data(self):
        return self.__data        
        
    def rrinterval(self, add_col=False, col_name='rri'):
        rri = 60000 / self.vals
        self.rri = rri
        if not add_col:
            return rri
        else:
            self.data[col_name] = rri
            return self.data
        
    def hrv_time_domain(self):
        if self.rri:
            rri = self.rri
        else:
            rri = self.rrinterval()
        rri = hrv.rri.RRi(rri)
        features = hrv.classical.time_domain(rri)
        return features
        
    def hrv_freq_domain(self, rri):
        rri = hrv.rri.RRi(rri)
        features = hrv.classical.frequency_domain(rri)
        return features


class BData(BaseBData):
    
    def __init__(self, data=None, vals=None, time=None):
        super(BData, self).__init__(data)
        self.__time_name = 'time'
        self.__vals_name = 'hr'
        if isinstance(data, pd.DataFrame):
            self.__data = data
            self.__time = self.data[self.time_name]
            self.__vals = self.data[self.vals_name]            
        elif isinstance(data, list):
            self.__time = data[0]
            self.__vals = data[1]
            self.__data = self._construct()
        else:
            raise ValueError('Input type error: must be dataframe or list')
    
    def __getitem__(self, position):
        if isinstance(position, (slice, np.ndarray)):
            return BData(self.__data[position])
        else:
            return self.__data[position]

    @property
    def vals(self):
        return self.__vals
        
    @property
    def time(self):
        return self.__time
        
    @property
    def data(self):
        return self.__data
        
    def sampling(label=None, **kwags):
        pass
        
       
def alignment_bdata(datas, keepdims=False, reset_index=True):
       
    ## TODO: modifier the code
#    flags = list(map(lambda data: isinstance(data.index, DatetimeIndex), datas))
#    try:
#        flags = flags.index(True)
#    except:
#        flags = None
#    # convert index to numeic.Int64Index
#    datas[flags] = list(map(lambda data: data.reset_index(drop=False),datas[flags]))
    # Data only contain time and vals
    datas = list(map(lambda data: data.groupby('time').mean(), datas))
    # Time alignment between different sensor datas in seconds level
    df = reduce(lambda data1,data2: pd.concat([data1, data2], axis=1), datas)
    df = df.reset_index(drop=False)
    if not keepdims:
        df = df.dropna()
    if reset_index:
        df = df.reset_index(drop=True)
    return df
    
                   
        