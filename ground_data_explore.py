# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:14:42 2020

@author: arnow
"""

import numpy as np
import matplotlib.pyplot as plt

names = np.genfromtxt('AL.Met_Od-DJOUGOU-2012.csv',delimiter=';')


sub_data = names[0:1000,2]
x = np.arange(0,1000,1)

fig, ax = plt.subplots()
ax.scatter(x,sub_data,marker=".")

plt.show()






#Namibia
gr_data = np.genfromtxt('NUST Hour.csv',delimiter=',',skip_header=4)
gr_data2 = np.genfromtxt('NUST Hour.csv',delimiter=',',dtype=str,skip_header=4)
sub_data = gr_data[0:200,5]
sub_data_2 = gr_data[1000:2200,5]
x = np.arange(0,200,1)

fig, ax = plt.subplots()
ax.scatter(x,sub_data,marker=".")
ax.scatter(x,sub_data_2,marker="o")
plt.show()


samp_dates = gr_data2[0:200,0]


import pandas as pd
from datetime import datetime


string_date_rng_2 = ['June-01-2018', 'June-02-2018', 'June-03-2018']
timestamp_date_rng_2 = [datetime.strptime(x,'%B-%d-%Y') for x in string_date_rng_2]
timestamp_date_rng_2

np.array(timestamp_date_rng_2)


timestamp_date_rng_2 = [datetime.strptime(x,'%d/%m/%Y %H:%M:%S') for x in samp_dates]
timestamp_date_rng_2


fig, ax = plt.subplots()
ax.scatter(timestamp_date_rng_2,sub_data,marker=".")
plt.show()






import seaborn as sns
import pandas as pd
from io import StringIO


textfile = StringIO("""fee,time
100,650
90,700
80,860
70,800
60,1000
50,1200""")

df = pd.read_csv(textfile)

_ = sns.lmplot(timestamp_date_rng_2, sub_data, data=df, ci=None)




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
csv = pd.read_csv('ee-chart_full_kumasi_AOD_utf8.csv')



data = csv[['system:time_start', 'Optical_Depth_047']]
x = data['system:time_start']

x_time = [datetime.strptime(i,'%b %d, %Y') for i in x]
n_time = dates.date2num(x_time)
y = data['Optical_Depth_047']
plt.scatter(n_time, y)

idx = np.isfinite(n_time) & np.isfinite(y)

z = np.polyfit(n_time[idx], y[idx], 1)



p = np.poly1d(z)
plt.plot(n_time,p(n_time),"r-")
plt.show()


#Data wrangling explore
#Sort data in issues
import os
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np

data_in = pd.read_csv("AL.Met_Od-DJOUGOU-2014.csv", header=None, nrows=5,sep=';') 

ds = Dataset("AL.Met_Od_DJOUGOU_201201010000_201710132345.nc")
print(ds)

for dim in ds.dimensions.values():
    print(dim)

print(ds['Incoming_Shortwave_Radiation'])
prcp = ds['Incoming_Shortwave_Radiation'][:]
prcp[0:100,0,0]
rad_in = np.array(prcp[0:5000,0,0])
tm = ds['time'][:][1:1000]

plt.plot(rad_in)


djo_data_pd.loc[0:23, 'swr_in']

















