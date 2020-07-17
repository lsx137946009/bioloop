#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 13:55:40 2020

@author: lsx
"""


class RevealAccess(object):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print('Retrieving', obj.y)
        object.__setattr__(obj, self.name, self.val)
        return self.val

#    def __set__(self, obj, val):
#        print('Updating', self.name)
#        self.val = val
        
class MyClass(object):
    
    x = RevealAccess(10, 'z')
    y = 5
    
m = MyClass()
m.x
print(m.x)
print(m.z)


#==============================================================================
# import pandas as pd
# A = {'name':['A','B','C','D','E'],
#      'sex': ['m','f','f','f','m']}
# A = pd.DataFrame(A)
# b = A.groupby('sex')
#==============================================================================

#==============================================================================
# import pandas as pd
# import numpy as np
# 
# class Method(object):
#     
#     def __init__(self, data):
#         self.data = data
#         
#     def bb(self):
#         return np.mean(self.data)
#         
# class MyData(pd.Series):
#         
#     def me(self):
#         return Method(self)
#         
# a = MyData([1,2]).me().bb()
#==============================================================================



