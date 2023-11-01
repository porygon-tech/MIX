#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 13:51:23 2023

@author: ubuntu
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import contextlib

def spyder_backend(io=True):
    if io:
        gui = 'module://matplotlib_inline.backend_inline'
    else: 
        gui = 'qt5agg'
    with contextlib.suppress(ValueError):
        matplotlib.use(gui, force=True)
    globals()['plt'] = matplotlib.pyplot


def norm(x, mu, sigma):
    return 1 / (sigma * np.sqrt(2*np.pi)) * np.exp(-0.5 * ((x - mu) / sigma)**2)

def rescale(arr, vmin=0,vmax=1):
    amin = np.min(arr)
    amax = np.max(arr)
    return  (arr - amin) / (amax - amin) * (vmax - vmin) +  vmin

#%%
spyder_backend(False)

x=np.linspace(-5,5,100)
y=norm(x,3,1)
plt.plot(x,y)

c=plt.cm.rainbow_r(rescale(x))
plt.plot(c)


#%%


x=np.linspace(-5,5,100)
y=norm(x,-3,2)*2
x=np.repeat(np.c_[x],500, axis=1)
c=plt.cm.rainbow_r(rescale(x))
#%%
spectre = np.c_[y][...,np.newaxis]*c
spectre =  spectre[...,:3]  # remove alpha channel
fig = plt.figure(figsize=(8,6)); ax = fig.add_subplot(111)
pos = ax.imshow(spectre,interpolation='None')
ax.invert_yaxis()
plt.tight_layout()
plt.show()

#%%
fig = plt.figure(figsize=(8,6)); ax = fig.add_subplot(111)
pos = ax.imshow(c,interpolation='None')
ax.invert_yaxis()
plt.tight_layout()
plt.show()
#%%

I = np.newaxis
avc = rescale(spectre[:,0,:].sum(0)[I,I,:])
avc = np.repeat(avc,10, axis=0)
avc = np.repeat(avc,10, axis=1)


fig = plt.figure(figsize=(2,2)); ax = fig.add_subplot(111)
pos = ax.imshow(avc,interpolation='None')
ax.invert_yaxis()
plt.tight_layout()
plt.show()
