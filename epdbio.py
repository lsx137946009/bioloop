#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 15:49:56 2020

@author: lsx
"""

import os
import pandas as pd

PATH_INFO = './infos.csv'
PATH_BAND = '/media/lsx/TOSHIBA EXT/吕小凤数据备份/D/epilepsy/h5/raw'
PATH_EVENT = '/media/lsx/TOSHIBA EXT/吕小凤数据备份/D/epilepsy/records/seizure43'


class DataBase(object):
    
    def connect(self,
                path_info=PATH_INFO,
                path_band=PATH_BAND,
                path_event=PATH_EVENT):
        self.idb = InfoDataBase().connect(path=path_info)
        self.bdb = BandDataBase().connect(path=path_band)
        self.edb = EventDataBase().connect(path=path_event)
        return self
        
    def load_info(self, name=None):
        info = self.idb.load(name)
        return info
        
    def load_bdata(self, name=None, stypes=['ac','gs','hr']):
        data = self.bdb.load(name, stypes=stypes)
        return data
        
    def load_event(self, name=None):
        event = self.edb.load(name)
        return event


class InfoDataBase(object):
       
    def connect(self, path=PATH_INFO):
        ## TODO: add notation 
        ## TODO: add database method
        """
            URL:
            PATH:
        """
        self.path = path
        return self
    
    def load(self, name=None):
        infos = pd.read_csv(self.path)
        if not name:
            return infos
        else:
            info = infos[infos.name==name]
            return info
        
    
class BandDataBase(object):
    
    def connect(self, path=PATH_BAND):
        ## TODO: add notation 
        ## TODO: add database method
        """
            URL:
            PATH:
        """
        self.path = path
        return self

    def load_unique(self, name, stype):
        if not isinstance(name, str):
            raise ValueError('name must be str')
        if not isinstance(stype, str):
            raise ValueError('stype must be str')
        pathData = os.path.join(self.path,name,str(stype+name+'.h5'))
        data = pd.read_hdf(pathData, 'df')
        data = data.drop(['name', 'id'], axis=1)
        return data
        
    def _load_batch_stypes(self, name, stypes=['ac','gs','hr']):
        try:
            stypes = list(stypes)
        except:
            raise ValueError('stype must be str or list(array-like)')
        datas = dict()
        for stype in stypes:
            try:
                data = self.load_unique(name, stype)
            except:
                continue
            datas[stype] = data
        return datas
    
    def _load_batch_names(self, names, stype):
        try:
            names = list(names)
        except:
            raise ValueError('names must be str or list(array-like)')
        datas = dict()
        for name in names:
            data = self.load_unique(name, stype)
            datas[name] = data
        return datas                       
            
    def load(self, names, stypes=['ac','gs','hr']):
        if isinstance(names, str):
            datas_single = self._load_batch_stypes(names, stypes)
            return datas_single
        else:
            try:
                names = list(names)
            except:
                raise ValueError('names must be str or list(array-like)')
            datas_multi = dict()
            for name in names:
                datas_single = self._load_batch_stypes(name, stypes)
                datas_multi[name] = datas_single
            return datas_multi
            
            
class EventDataBase(object):
    
    def connect(self, path=PATH_EVENT):
        ## TODO: add notation 
        ## TODO: add database method
        """
            URL:
            PATH:
        """
        self.path = path
        return self
        
    def load(self, name, event_type='seizure'):
        ## TODO: add more type
        event_path = os.path.join(self.path, str(name+'.csv'))
        event = pd.read_csv(event_path, sep=',', header=None)
        event.columns = ['event_start', 'event_end']
        event['event_start'] = pd.to_datetime(event['event_start'])
        event['event_end'] = pd.to_datetime(event['event_end'])
        event = event.dropna()
        return event            