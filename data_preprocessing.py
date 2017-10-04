#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 01:29:37 2017

@author: mikeias
"""

def scale(dataset):
    from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    return sc_X.fit_transform(dataset)