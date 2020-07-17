#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 17:34:00 2020

@author: lsx
"""

import patient
import window
import bdata
import event
import pandas as pd
import feature
import preprocessing


names = ['ChaiXinyu', 'ChenBolin']

feas = dict()
for name in names:
    ### Test patient
    p = patient.Patient(name, stypes=['ac','hr','gy'])
    datas = p.data
    datas = bdata.alignment_bdata(list(datas.values()))
    
    ### Test preprocessing
    outlier = preprocessing.DropOutliersCI(keepdims=True,reset_index=True)
    col_vals = list(datas.columns)
    col_vals.remove('time')
    for col in col_vals:
        datas[col] = outlier.fit_transform(datas[col])   
    datas = datas.dropna()
    
    data_ac = bdata.BDataThreeAxis(datas[['time','ac1','ac2','ac3']])
    data_hr = bdata.BDataHeartRate(datas[['time','hr']])
    datas['mod'] = data_ac.modulus()
    datas['rri'] = data_hr.rrinterval()
    print(p.info)
    
    ### Test event
    event_seizure = event.mark_event_seizure(datas['time'], p.event, buff=300)
    datas = pd.merge(datas, event_seizure)
    datas = datas.set_index('time')
    
    ### Test window
    sldwin = window.SlidingWindow(window=300, overlap=0, min_size=150,
                       normalize=True, closed='left')
    #windows = sldwin.slice_dataframe(datas)
    
    def window_func(win):
        col_time = 'time'
        col_vals = list(win.columns)
        col_vals.remove('time')
        col_vals.remove('event_seizure')
        col_event = 'event_seizure'
        time = win[col_time]
        vals = win[col_vals]
        event = win[col_event]
        ## TODO: problem with data stack if add info data
        func = feature.Feature(time=time, vals=vals, event=event).func()
        return func
    
    #feas = windows.apply(window_func)
    fea = sldwin.slice_dataframe(datas).apply(window_func)
    fea['name'] = p.name
    fea['sex']  = p.sex
    fea['age']  = p.age
    feas.update({name: fea})
