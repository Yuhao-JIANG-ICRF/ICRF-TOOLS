#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 14:27:07 2025

@author: YJ281217
"""
import numpy as np
import matplotlib.pyplot as plt

def f1(Ne,Zi,Xi,Ai):
    fv = Ne*Xi*Zi**2/(Ne*Ai)
    return fv

X_H = 0.05
X_D = 0.50

X_T = 1-X_D-X_H

Z_D = 2
a_D = 1
Z_T = 3
a_T = 1
Z_H = 1
a_H = 1

Te = 10e3
Ne = 1.5e20
Af = a_H 

Ec = 14.8*Te*Af*(  f1(Ne,Z_T,X_T,a_T)
                 + f1(Ne,Z_D,X_D,a_D)
                 + f1(Ne,Z_H,X_T,a_H))**(2/3)

print(Ec/1e3)