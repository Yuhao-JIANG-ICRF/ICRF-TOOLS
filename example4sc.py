# %%
## cleaning in SPYDER
get_ipython().magic('reset -f')
get_ipython().magic('clear')
##
globals().clear()
import numpy as np
import matplotlib.pyplot as plt
from load import fun_load_touchstone as flt
from smith_chart import smith_Smatrix
import gc as gc

gc.collect()    #release ram
plt.close('all')     #close all figures

# %% data file
pre = 'input/example/'
fname = 'smatrix_aug-like.s4p'
fre_unit = 'Hz'
# %% read data
fre_units = {'MHz':1e6,'Hz':1}
fre_u = fre_units[fre_unit]
#load s4p file, trans to freauency and Smatrix
fre,S = flt(pre+fname)
fre = fre*fre_u
# %% set the data
x= fre
S11 = np.array([Smatrix[0,0] for Smatrix in S])
# %% plot smith chart
a = len(fre)
smith_Smatrix(S11, 1,display_mode='line_with_arrow')
plt.show()
