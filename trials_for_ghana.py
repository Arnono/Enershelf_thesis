# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 22:35:00 2020

@author: arnow
"""


#Ground station data
import os
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

import matplotlib.dates as dates

import requests
import json


# =============================================================================
# 
# Station trend data and visuaizations
# =============================================================================


#Benin

#pv watts
os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data\\benin')
data_ben_pvwatts = pd.read_csv("pvwatts_ben.csv",sep=',')
data_ben_pvwatts["Plane of Array Irradiance (W/m^2)"]
data_ben_pvwatts = data_ben_pvwatts.drop(columns=["Month","Day","Hour","Beam Irradiance (W/m^2)",
                                                "Diffuse Irradiance (W/m^2)","Ambient Temperature (C)",
                                                "Wind Speed (m/s)","Cell Temperature (C)","DC Array Output (W)",
                                                "AC System Output (W)"])
data_ben_pvwatts["time"] = pd.date_range(start='1/1/2015', end='1/1/2016',freq='H')[:-1]
pvwatts_ben_df_period = data_ben_pvwatts.groupby(data_ben_pvwatts["time"].dt.week)["Plane of Array Irradiance (W/m^2)"].mean()

#Yearly aggregates
ig, axs = plt.subplots(figsize=(12, 4))
data_ben_pvwatts.groupby(data_ben_pvwatts["time"].dt.week)["Plane of Array Irradiance (W/m^2)"].mean().plot(kind='bar',rot=0,ax=axs)
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Radiation (w/m^2)$");



#os.getcwd()
os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data\\benin')
met_data_djo = Dataset("AL.Met_Od_DJOUGOU_201201010000_201710132345.nc")

print(met_data_djo)

time_djo = met_data_djo['time'][:]
in_swr_djo = met_data_djo['Incoming_Shortwave_Radiation'][:]

#As np arrays
time_djo_arr = np.array(time_djo)
time_dt_djo = [datetime.fromtimestamp(x) for x in time_djo] #Correct time formart

in_swr_djo_arr = np.array(in_swr_djo[:,0,0])
in_swr_djo_arr[(in_swr_djo_arr > 5000) | (in_swr_djo_arr < -100)] = float("NAN")

#Check data plots
plt.scatter(time_dt_djo[0:1000], in_swr_djo_arr[0:1000])

#Convert to Pandas DF
djo_data = np.stack((time_djo, in_swr_djo_arr), axis=1)
djo_data_pd = pd.DataFrame(data=djo_data, columns=["time", "swr_in"], dtype='float')

djo_data_pd["time2"] = time_dt_djo

#Normalization *100
djo_data_pd["swr_in_norm"]=((djo_data_pd["swr_in"]-djo_data_pd["swr_in"].min())/(djo_data_pd["swr_in"].max()-djo_data_pd["swr_in"].min()))*100
djo_df_period = djo_data_pd.groupby(djo_data_pd["time2"].dt.week)["swr_in_norm"].mean()
djo_df_period_org = djo_data_pd.groupby(djo_data_pd["time2"].dt.week)["swr_in"].mean()

#Yearly aggregates
ig, axs = plt.subplots(figsize=(12, 4))
djo_data_pd.groupby(djo_data_pd["time2"].dt.week)["swr_in"].mean().plot(kind='bar',rot=0,ax=axs)
plt.xlabel("Hour of the day");  # custom x label using matplotlib
plt.ylabel("$NO_2 (µg/m^3)$");



#Benin _GNONGANBI
#os.getcwd()
met_data_gno = Dataset("AL.Met_Od_GNONGANBI_201407211645_201710132345.nc")

print(met_data_djo)

time_ngo = met_data_gno['time'][:]
in_swr_ngo = met_data_gno['Incoming_Shortwave_Radiation'][:]

#As np arrays
time_ngo_arr = np.array(time_ngo)
time_dt_ngo = [datetime.fromtimestamp(x) for x in time_ngo] #Correct time formart

in_swr_ngo_arr = np.array(in_swr_ngo[:,0,0])
in_swr_ngo_arr[(in_swr_ngo_arr > 5000) | (in_swr_ngo_arr < -100)] = float("NAN")

#Check data plots
plt.scatter(time_dt_ngo[0:1000], in_swr_ngo_arr[0:1000])

#Convert to Pandas DF
ngo_data = np.stack((time_ngo, in_swr_ngo_arr), axis=1)
ngo_data_pd = pd.DataFrame(data=ngo_data, columns=["time", "swr_in"], dtype='float')

ngo_data_pd["time2"] = time_dt_ngo

#Normalization *100
ngo_data_pd["swr_in_norm"]=((ngo_data_pd["swr_in"]-ngo_data_pd["swr_in"].min())/(ngo_data_pd["swr_in"].max()-ngo_data_pd["swr_in"].min()))*100
ngo_df_period = ngo_data_pd.groupby(ngo_data_pd["time2"].dt.week)["swr_in_norm"].mean()
ngo_df_period_org = ngo_data_pd.groupby(ngo_data_pd["time2"].dt.week)["swr_in"].mean()

#Yearly aggregates
ig, axs = plt.subplots(figsize=(12, 4))
z_df = ngo_data_pd.groupby(ngo_data_pd["time2"].dt.month)["swr_in"].mean().plot(kind='bar',rot=0,ax=axs)
plt.xlabel("Hour of the day");  # custom x label using matplotlib
plt.ylabel("$NO_2 (µg/m^3)$");



#Niger 
#os.getcwd()
os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data\\niger')
met_data_ban = Dataset("AL.Met_Nc_BANIZOUMBOU_200501010000_201512312345.nc")

print(met_data_ban)

time_ban = met_data_ban['time'][:]
in_swr_ban = met_data_ban['Incoming_Shortwave_Radiation'][:]

#As np arrays
time_ban_arr = np.array(time_ban)
time_dt_ban = [datetime.fromtimestamp(x) for x in time_ban] #Correct time formart

in_swr_ban_arr = np.array(in_swr_ban[:,0,0])
in_swr_ban_arr[(in_swr_ban_arr > 5000) | (in_swr_ban_arr < -100)] = float("NAN")

#Check data plots
plt.scatter(time_dt_ban[0:1000], in_swr_ban_arr[0:1000])

#Convert to Pandas DF
ban_data = np.stack((time_ban, in_swr_ban_arr), axis=1)
ban_data_pd = pd.DataFrame(data=ban_data, columns=["time", "swr_in"], dtype='float')

ban_data_pd["time2"] = time_dt_ban

#Normalization *100
ban_data_pd["swr_in_norm"]=((ban_data_pd["swr_in"]-ban_data_pd["swr_in"].min())/(ban_data_pd["swr_in"].max()-ban_data_pd["swr_in"].min()))*100
ban_df_period = ban_data_pd.groupby(ban_data_pd["time2"].dt.week)["swr_in_norm"].mean()
ban_df_period_org = ban_data_pd.groupby(ban_data_pd["time2"].dt.week)["swr_in"].mean()

#Yearly aggregates
ig, axs = plt.subplots(figsize=(12, 4))
z_df = ban_data_pd.groupby(ban_data_pd["time2"].dt.week)["swr_in"].mean().plot(kind='bar',rot=0,ax=axs)
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Radiation (w/m^3)$");



#senegal 
#pv watts
os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data\\senegal')
data_in_pvwatts = pd.read_csv("pvwatts_sen.csv",sep=',')
data_in_pvwatts["Plane of Array Irradiance (W/m^2)"]
data_in_pvwatts = data_in_pvwatts.drop(columns=["Month","Day","Hour","Beam Irradiance (W/m^2)",
                                                "Diffuse Irradiance (W/m^2)","Ambient Temperature (C)",
                                                "Wind Speed (m/s)","Cell Temperature (C)","DC Array Output (W)",
                                                "AC System Output (W)"])
data_in_pvwatts["time"] = pd.date_range(start='1/1/2015', end='1/1/2016',freq='H')[:-1]
pvwatts_sen_df_period = data_in_pvwatts.groupby(data_in_pvwatts["time"].dt.week)["Plane of Array Irradiance (W/m^2)"].mean()

#Yearly aggregates
ig, axs = plt.subplots(figsize=(12, 4))
data_in_pvwatts.groupby(data_in_pvwatts["time"].dt.week)["Plane of Array Irradiance (W/m^2)"].mean().plot(kind='bar',rot=0,ax=axs)
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Radiation (w/m^2)$");


#_fatickifcqc
os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data\\senegal')
data_in = pd.read_csv("solar-measurementssenegal-fatickifcqc.csv",sep=';') 

time_df = data_in['time']  
data_in = data_in.drop(columns=['time','relative_humidity','barometric_pressure','wind_speed','wind_speed_calc','wind_from_direction','sensor_cleaning','comments'])
data_in_fl = data_in.astype(float)

data_in["time"] = pd.to_datetime(time_df)

#Normalization *100
fat_data_pd = data_in
fat_data_pd["ghi_sil_norm"]=((data_in["ghi_sil"]-data_in["ghi_sil"].min())/(data_in["ghi_sil"].max()-data_in["ghi_sil"].min()))*100
fat_df_period = data_in.groupby(data_in["time"].dt.week)["ghi_sil_norm"].mean()
fat_df_period_org = data_in.groupby(data_in["time"].dt.week)["ghi_sil"].mean()

#Yearly aggregates
ig, axs = plt.subplots(figsize=(12, 4))
data_in.groupby(data_in["time"].dt.month)["ghi_sil"].mean().plot(kind='bar',rot=0,ax=axs)
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Radiation (w/m^2)$");



#_kahoneifcqc
os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data\\senegal')
data_in = pd.read_csv("solar-measurementssenegal-kahoneifcqc.csv",sep=';') 

time_df = data_in['time']  
data_in = data_in.drop(columns=['time','relative_humidity','barometric_pressure','wind_speed','wind_speed_calc','wind_from_direction','sensor_cleaning','comments'])
data_in_fl = data_in.astype(float)

data_in["time"] = pd.to_datetime(time_df)

#Normalization *100
kah_data_pd = data_in
kah_data_pd["ghi_sil_norm"]=((data_in["ghi_sil"]-data_in["ghi_sil"].min())/(data_in["ghi_sil"].max()-data_in["ghi_sil"].min()))*100
kah_df_period = data_in.groupby(data_in["time"].dt.week)["ghi_sil_norm"].mean()
kah_df_period_org = data_in.groupby(data_in["time"].dt.week)["ghi_sil"].mean()

#Yearly aggregates
ig, axs = plt.subplots(figsize=(12, 4))
data_in.groupby(data_in["time"].dt.week)["ghi_sil"].mean().plot(kind='bar',rot=0,ax=axs)
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Radiation (w/m^3)$");


#_toubaifcqc
os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data\\senegal')
data_in = pd.read_csv("solar-measurementssenegal-toubaifcqc.csv",sep=';') 

time_df = data_in['time']  
data_in = data_in.drop(columns=['time','relative_humidity','barometric_pressure','wind_speed','wind_speed_calc','wind_from_direction','sensor_cleaning','comments'])
data_in_fl = data_in.astype(float)

data_in["time"] = pd.to_datetime(time_df)

#Normalization *100
tou_data_pd = data_in
tou_data_pd["ghi_sil_norm"]=((data_in["ghi_sil"]-data_in["ghi_sil"].min())/(data_in["ghi_sil"].max()-data_in["ghi_sil"].min()))*100
tou_df_period = data_in.groupby(data_in["time"].dt.week)["ghi_sil_norm"].mean()
tou_df_period_org = data_in.groupby(data_in["time"].dt.week)["ghi_sil"].mean()

#Yearly aggregates
ig, axs = plt.subplots(figsize=(12, 4))
data_in.groupby(data_in["time"].dt.week)["ghi_sil"].mean().plot(kind='bar',rot=0,ax=axs)
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Radiation (w/m^3)$");

# =============================================================================
# 
# All stationa 
# =============================================================================

ig, axs = plt.subplots(figsize=(10, 6))
plt.step(list(djo_df_period.index.values),djo_df_period, where='mid')
plt.step(list(ngo_df_period.index.values),ngo_df_period, where='mid')
plt.step(list(ban_df_period.index.values),ban_df_period, where='mid')
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Elec");


ig, axs = plt.subplots(figsize=(10, 6))
plt.step(list(fat_df_period.index.values),fat_df_period, where='mid')
plt.step(list(kah_df_period.index.values),kah_df_period, where='mid')
plt.step(list(tou_df_period.index.values),tou_df_period, where='mid')
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Elec");


#Original data

ig, axs = plt.subplots(figsize=(10, 6))
plt.step(list(djo_df_period_org.index.values),djo_df_period_org, where='mid',label='Djo')
plt.step(list(ngo_df_period_org.index.values),ngo_df_period_org, where='mid',label='Gno')
plt.step(list(ban_df_period_org.index.values),ban_df_period_org, where='mid',label='Ban')
plt.legend(title='Data source:')
plt.title("Ground data 1")
plt.xlabel("Time in weeks");  # custom x label using matplotlib
plt.ylabel("Irradiation (W/m^2)");


ig, axs = plt.subplots(figsize=(10, 6))
plt.step(list(fat_df_period_org.index.values),fat_df_period_org, where='mid',label='Fat')
plt.step(list(kah_df_period_org.index.values),kah_df_period_org, where='mid',label='Kah')
plt.step(list(tou_df_period_org.index.values),tou_df_period_org, where='mid',label='Tou')
plt.legend(title='Data source:')
plt.title("Ground data 2")
plt.xlabel("Time in weeks");  # custom x label using matplotlib
plt.ylabel("Irradiation (W/m^2)");



# =============================================================================
# 
# Variable time series tracking and visuaizations
# =============================================================================

#Kumasi station
#Atmospheric optical depth_Modis
os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data')
csv = pd.read_csv('ee-chart_full_kumasi_AOD_utf8.csv')


data = csv[['system:time_start', 'Optical_Depth_047']]

#Sorting datetime
x = data['system:time_start']
x_time = [datetime.strptime(i,'%b %d, %Y') for i in x]
n_time = dates.date2num(x_time)

y = data['Optical_Depth_047']

idx = np.isfinite(n_time) & np.isfinite(y)
z = np.polyfit(n_time[idx], y[idx], 1)
p = np.poly1d(z)

plt.scatter(x_time, y,marker='.')
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("AOD");

plt.plot(n_time,p(n_time),c= "orange")
plt.show()

#Change data types
csv = csv.drop(columns=['system:time_start'])
csv_fl = csv.astype(float)
csv_fl["time"] = x_time

#Yearly aggregates
ig, axs = plt.subplots(figsize=(10, 6))
csv_fl.groupby(csv_fl["time"].dt.month)["Optical_Depth_047"].mean().plot(kind='bar',rot=0,ax=axs)
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("AOD");




#Precipitation ERA5
os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data')
csv = pd.read_csv('ee-chart_kumasi_prep_2.csv')

data = csv[['system:time_start', 'total_precipitation']]

#Sorting datetime
x = data['system:time_start']
x_time = [datetime.strptime(i,'%b %d, %Y') for i in x]
n_time = dates.date2num(x_time)

y = data['total_precipitation']

idx = np.isfinite(n_time) & np.isfinite(y)
z = np.polyfit(n_time[idx], y[idx], 1)
p = np.poly1d(z)

plt.scatter(x_time, y,marker='.')
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Precipitation");

plt.plot(n_time,p(n_time),c= "orange")
plt.show()

#Change data types
csv = csv.drop(columns=['system:time_start'])
csv_fl = csv.astype(float)
csv_fl["time"] = x_time

#Yearly aggregates
ig, axs = plt.subplots(figsize=(10, 6))
csv_fl.groupby(csv_fl["time"].dt.week)["total_precipitation"].mean().plot(kind='bar',rot=0,ax=axs)
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("precipitation");





# =============================================================================
# 
# Ninja Data
# =============================================================================
#Djougou

token = '9a0117c2c0f94bc1d058d93d3ecbc704ab557b6f'
api_base = 'https://www.renewables.ninja/api/'

s = requests.session()
s.headers = {'Authorization': 'Token ' + token}

url = api_base + 'data/pv'
args = {
    'lat': 9.692,
    'lon': 1.6615,
    'date_from': '2016-01-01',
    'date_to': '2016-12-31',
    'dataset': 'merra2',
    'capacity': 1.0,
    'system_loss': 0.1,
    'tracking': 0,
    'tilt': 35,
    'azim': 180,
    'format': 'json'
}

r = s.get(url, params=args)

parsed_response = json.loads(r.text)

data = pd.read_json(json.dumps(parsed_response['data']), orient='index')
metadata = parsed_response['metadata']
data["time"] = list(data.index.values)
data["electricity_si"] = data["electricity"]*1000

#Normalization *100
data["electricity_norm"]=((data["electricity"]-data["electricity"].min())/(data["electricity"].max()-data["electricity"].min()))*100

# _aggregates
ig, axs = plt.subplots(figsize=(10, 6))
data.groupby(data["time"].dt.quarter)["electricity_si"].mean().plot(kind='bar',rot=0,ax=axs)
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Radiation (w/m^3)$");


ninja_sim_days = data.groupby(data["time"].dt.dayofyear)["electricity_si"].mean()

ig, axs = plt.subplots(figsize=(10, 6))
plt.step(list(ninja_sim_days.index.values),ninja_sim_days, where='mid')
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Elec");



#quarter dayofyear 



# Real vs sim data
data_sim_periods = data.groupby(data["time"].dt.month)["electricity_si"].mean()

ig, axs = plt.subplots(figsize=(10, 6))
plt.step(list(data_sim_periods.index.values),data_sim_periods, where='mid')
plt.step(list(djo_df_period_org.index.values),djo_df_period_org, where='mid')
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Elec");




# =============================================================================
# 
# 
# =============================================================================

import pvlib
from pvlib import clearsky, atmosphere, solarposition
from pvlib.location import Location




#SAHAR manual pull
os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data\\benin')
data_in = pd.read_csv("Timeseries_9.692_1.661_SA_1kWp_crystSi_14_30deg_-179deg_2014_2016_djo.csv",sep=',',
                      skip_blank_lines=True,header = 8,skipfooter=12) 

time_arr = np.array(data_in['time']) 
time_dtf = [datetime.strptime(x,'%Y%m%d:%H%M') for x in time_arr]
data_in["time"] = time_dtf

df_period_grp = data_in.groupby(data_in["time"].dt.week)["Gb(i)"].mean()


















