# -*- coding: utf-8 -*-
"""
Load Igor Pro
=============
"""


from pyscan import ItemAttribute
import igor.igorpy
import numpy as np


def load_igorpro(file_name,store_dim=True):
    igorwave = igor.binarywave.load(file_name)
    
    ds = ItemAttribute()
    ds.r = igorwave['wave']['wData']
    
    ds.runinfo = ItemAttribute()
    ds.runinfo.sweep_name= ['xgate']
    ds.runinfo.step_name = ['ygate']

    nx, ny = np.shape(ds.r)
    
    dx = igorwave['wave']['wave_header']['sfA'][0]
    dy = igorwave['wave']['wave_header']['sfA'][1]
    x0 = igorwave['wave']['wave_header']['sfB'][0]
    y0 = igorwave['wave']['wave_header']['sfB'][1]
    
    ds.r = np.transpose(ds.r)
    
    if store_dim:
        ds.runinfo.xgate = np.arange(x0, x0+nx*dx, dx)
        ds.runinfo.ygate = np.arange(y0, y0+ny*dy, dy)
    else:
        dv = 0.001
    
        ds.runinfo.xgate = np.arange(0, dv*(nx-1), dv)
        ds.runinfo.ygate = np.arange(0, dv*(ny-1), dv)

    ds.xgate, ds.ygate = np.meshgrid(ds.runinfo.xgate, ds.runinfo.ygate)

    return ds
