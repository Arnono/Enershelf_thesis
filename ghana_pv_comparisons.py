# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 09:48:08 2020

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
from pvlib import location
from pvlib import irradiance
from scipy import stats



# =============================================================================
# 
# Station trend data and visuaizations
# =============================================================================




#Benin
os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data\\benin')

#_djo
latitude = 9.692
longitude = 1.6615
met_data_djo = Dataset("AL.Met_Od_DJOUGOU_201201010000_201710132345.nc")

#gno
# latitude = 9.7421
# longitude = 1.802
# met_data_djo = Dataset("AL.Met_Od_GNONGANBI_201407211645_201710132345.nc")

#Ban
# latitude = 13.5311
# longitude = 2.6613
# os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data\\niger')
# met_data_djo = Dataset("AL.Met_Nc_BANIZOUMBOU_200501010000_201512312345.nc")



time_djo = met_data_djo['time'][:]
in_swr_djo = met_data_djo['Incoming_Shortwave_Radiation'][:]

#As np arrays
time_djo_arr = np.array(time_djo)
time_dt_djo = [datetime.fromtimestamp(x) for x in time_djo] #Correct time formart

in_swr_djo_arr = np.array(in_swr_djo[:,0,0])
in_swr_djo_arr[(in_swr_djo_arr > 5000) | (in_swr_djo_arr < -100)] = float("NAN")

#Convert to Pandas DF
djo_data = np.stack((time_djo, in_swr_djo_arr), axis=1)
djo_data_pd = pd.DataFrame(data=djo_data, columns=["time", "swr_in"], dtype='float')
djo_data_pd["time2"] = time_dt_djo

djo_df_period_org = djo_data_pd.groupby(djo_data_pd["time2"].dt.week)["swr_in"].mean()





#Senegal
# os.chdir('C:\\rli\\ghana_project\\source_data\\ground_pv_data\\senegal')

#_fatickifcqc
# latitude = 14.36751
# longitude = -16.41346
# data_in = pd.read_csv("solar-measurementssenegal-fatickifcqc.csv",sep=';') 

# latitude = 14.168636
# longitude = -16.034167
# data_in = pd.read_csv("solar-measurementssenegal-kahoneifcqc.csv",sep=';')

# latitude = 14.77252
# longitude = -15.91955
# data_in = pd.read_csv("solar-measurementssenegal-toubaifcqc.csv",sep=';') 

# time_df = data_in['time']  
# data_in = data_in.drop(columns=['time','relative_humidity','barometric_pressure','wind_speed','wind_speed_calc','wind_from_direction','sensor_cleaning','comments'])
# data_in["time"] = pd.to_datetime(time_df)

# fat_df_period_org = data_in.groupby(data_in["time"].dt.week)["ghi_sil"].mean()
# djo_df_period_org = fat_df_period_org










ig, axs = plt.subplots(figsize=(10, 6))
plt.step(list(djo_df_period_org.index.values),djo_df_period_org, where='mid')
plt.xlabel("Time in weeks");  # custom x label using matplotlib
plt.ylabel("Irradiation (W/m^2)$");


# =============================================================================
# 
# Clear Sky
# =============================================================================

tz = 'Europe/Berlin'
lat, lon = latitude, longitude

site = location.Location(lat, lon, tz=tz)


def get_irradiance(site_location, tilt, surface_azimuth):
    times = pd.date_range(start='1/1/2015', end='1/1/2016',freq='H',tz=site_location.tz)
    clearsky = site_location.get_clearsky(times)
    solar_position = site_location.get_solarposition(times=times)
    POA_irradiance = irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=surface_azimuth,
        dni=clearsky['dni'],
        ghi=clearsky['ghi'],
        dhi=clearsky['dhi'],
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth'])
    return pd.DataFrame({'GHI': clearsky['ghi'],
                         'POA': POA_irradiance['poa_global']})


pvlib_sim_clear = get_irradiance(site, 30, 180)
pvlib_sim_clear["time"] = list(pvlib_sim_clear.index.values)

pvlib_sim_clear_DAILY = pvlib_sim_clear.groupby(pvlib_sim_clear["time"].dt.week)["GHI"].mean()

ig, axs = plt.subplots(figsize=(10, 6))
plt.step(list(pvlib_sim_clear_DAILY.index.values),pvlib_sim_clear_DAILY, where='mid')
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Elec");

# =============================================================================
# 
# Ninja data
# =============================================================================


token = '9a0117c2c0f94bc1d058d93d3ecbc704ab557b6f'
api_base = 'https://www.renewables.ninja/api/'

s = requests.session()
s.headers = {'Authorization': 'Token ' + token}

url = api_base + 'data/pv'
args = {
    'lat': latitude,
    'lon': longitude,
    'date_from': '2015-01-01',
    'date_to': '2015-12-31',
    'dataset': 'merra2',
    'capacity': 1.0,
    'system_loss': 0,
    'tracking': 0, #0.1
    'tilt': 30,
    'azim': 180,
    'format': 'json'
}

r = s.get(url, params=args)

parsed_response = json.loads(r.text)

data = pd.read_json(json.dumps(parsed_response['data']), orient='index')
metadata = parsed_response['metadata']
data["time"] = list(data.index.values)
data["electricity_si"] = data["electricity"]*1000

# _aggregates
#ig, axs = plt.subplots(figsize=(10, 6))
##data.groupby(data["time"].dt.week)["electricity_si"].mean().plot(kind='bar',rot=0,ax=axs)
#plt.xlabel("Time");  # custom x label using matplotlib
#plt.ylabel("Radiation (w/m^3)$");

ninja_sim_days = data.groupby(data["time"].dt.dayofyear)["electricity_si"].mean()
ninja_sim_week = data.groupby(data["time"].dt.week)["electricity_si"].mean()

#
ig, axs = plt.subplots(figsize=(10, 6))
plt.step(list(ninja_sim_week.index.values),ninja_sim_week, where='mid')
plt.xlabel("Time");  # custom x label using matplotlib
plt.ylabel("Elec");


# =============================================================================
# 
# SARAH
# =============================================================================

pvgis_url = "https://re.jrc.ec.europa.eu/api/seriescalc"

args = {
    'lat': latitude,
    'lon': longitude,
    'startyear': 2015,
    'endyear': 2015,
    'outputformat':'json',
    'pvcalculation':1,
    'peakpower':1,
    'loss':0 #10
}

pvgis_get = requests.get(pvgis_url, params = args)
pvgis_parsed_response = pvgis_get.json()

inputs = pvgis_parsed_response['inputs']
meta = pvgis_parsed_response['meta']
hourly_data = pvgis_parsed_response['outputs']['hourly']
pvgis_data = pd.DataFrame(hourly_data)
pvgis_data["time"] = pd.to_datetime(pvgis_data['time'], format='%Y%m%d:%H%M', utc=True)
#pvgis_data["P"]

pvgis_df_period_grp = pvgis_data.groupby(pvgis_data["time"].dt.week)["P"].mean()


ig, axs = plt.subplots(figsize=(10, 6))
plt.step(list(pvgis_df_period_grp.index.values),pvgis_df_period_grp, where='mid', label='SARAH')
plt.legend(title='Data source:')
plt.title("Comparison plot Kahone")
plt.xlabel("Time in weeks");  # custom x label using matplotlib
plt.ylabel("Irradiation (W/m^2)");



# =============================================================================
# 
#  
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


# =============================================================================
# 
# 
# =============================================================================

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

# =============================================================================
# 
# 
# =============================================================================


ig, axs = plt.subplots(figsize=(10,6))
plt.step(list(djo_df_period_org.index.values),djo_df_period_org, where='mid', label='Measured GHI',linewidth=3.0) 
plt.step(list(pvlib_sim_clear_DAILY.index.values),pvlib_sim_clear_DAILY,where='mid', label='Clear sky')
plt.step(list(pvgis_df_period_grp.index.values),pvgis_df_period_grp, where='mid', label='SARAH')
plt.legend(frameon=False)
plt.xlabel("Time in weeks",fontsize=16)  # custom x label using matplotlib
plt.ylabel("Irradiation (W/$m^2$)",fontsize=16)


ig, axs = plt.subplots(figsize=(10,6))
plt.bar(list(pvgis_df_period_grp.index.values),(djo_df_period_org-pvgis_df_period_grp))
plt.xlabel("Time in weeks",fontsize=16)  # custom x label using matplotlib
plt.ylabel("Delta Irradiation (W/$m^2$)",fontsize=16)

sum((djo_df_period_org-pvgis_df_period_grp)[:-1])




ig, axs = plt.subplots(figsize=(10, 6))
plt.step(list(djo_df_period_org.index.values),djo_df_period_org, where='mid', label='Measured GHI',linewidth=3.0) 
plt.step(list(pvlib_sim_clear_DAILY.index.values),pvlib_sim_clear_DAILY,where='mid', label='Clear sky')
plt.step(list(ninja_sim_week.index.values),ninja_sim_week, where='mid',label='Ninja')
plt.legend(frameon=False)
plt.xlabel("Time in weeks",fontsize=16)  # custom x label using matplotlib
plt.ylabel("Irradiation (W/$m^2$)",fontsize=16)

ig, axs = plt.subplots(figsize=(10,6))
plt.bar(list(djo_df_period_org.index.values),((djo_df_period_org-ninja_sim_week)[:-1]))
plt.xlabel("Time in weeks",fontsize=16)  # custom x label using matplotlib
plt.ylabel("Delta Irradiation (W/$m^2$)",fontsize=16)

sum((djo_df_period_org-ninja_sim_week)[:-1])




# ig, axs = plt.subplots(figsize=(10, 6))
# plt.step(list(djo_df_period_org.index.values),djo_df_period_org, where='mid', label='Measured GHI',linewidth=3.0) 
# plt.step(list(pvlib_sim_clear_DAILY.index.values),pvlib_sim_clear_DAILY,where='mid', label='Clear sky')
# plt.step(list(pvwatts_ben_df_period.index.values),pvwatts_ben_df_period, where='mid', label='NREL')
# plt.legend(frameon=False)
# plt.xlabel("Time in weeks",fontsize=16)  # custom x label using matplotlib
# plt.ylabel("Irradiation (W/$m^2$)",fontsize=16)

# ig, axs = plt.subplots(figsize=(10,6))
# plt.bar(list(djo_df_period_org.index.values),(djo_df_period_org-pvwatts_ben_df_period))
# plt.xlabel("Time in weeks",fontsize=16)  # custom x label using matplotlib
# plt.ylabel("Delta Irradiation (W/$m^2$)",fontsize=16)

# sum(djo_df_period_org-pvwatts_ben_df_period)



ig, axs = plt.subplots(figsize=(10, 6))
plt.step(list(djo_df_period_org.index.values),djo_df_period_org, where='mid', label='Measured GHI',linewidth=3.0) 
plt.step(list(pvlib_sim_clear_DAILY.index.values),pvlib_sim_clear_DAILY,where='mid', label='Clear sky')
plt.step(list(pvwatts_sen_df_period.index.values),pvwatts_sen_df_period, where='mid', label='NREL')
plt.legend(frameon=False)
plt.xlabel("Time in weeks",fontsize=16)  # custom x label using matplotlib
plt.ylabel("Irradiation (W/$m^2$)",fontsize=16)

ig, axs = plt.subplots(figsize=(10,6))
plt.bar(list(djo_df_period_org.index.values),((djo_df_period_org-pvwatts_sen_df_period)[:-1]))
plt.xlabel("Time in weeks",fontsize=16)  # custom x label using matplotlib
plt.ylabel("Delta Irradiation (W/$m^2$)",fontsize=16)

sum((djo_df_period_org-pvwatts_sen_df_period)[:-1])







ig, axs = plt.subplots(figsize=(8, 8))
plt.scatter(djo_df_period_org,pvgis_df_period_grp)
plt.scatter(djo_df_period_org,ninja_sim_week)
plt.scatter(djo_df_period_org,pvwatts_ben_df_period)



plt.plot(list(djo_df_period_org.index.values),djo_df_period_org)


stats.pearsonr(djo_df_period_org,pvlib_sim_clear_DAILY)

stats.pearsonr(djo_df_period_org,pvgis_df_period_grp)
stats.pearsonr(djo_df_period_org,ninja_sim_week)
stats.pearsonr(djo_df_period_org,pvwatts_ben_df_period)

# [:-1]
stats.pearsonr(djo_df_period_org,pvlib_sim_clear_DAILY[:-1])

stats.pearsonr(djo_df_period_org,pvgis_df_period_grp[:-1])
stats.pearsonr(djo_df_period_org,ninja_sim_week[:-1])
stats.pearsonr(djo_df_period_org,pvwatts_sen_df_period[:-1])



np.array(djo_df_period_org)
np.array(pvlib_sim_clear_DAILY)



plt.hist(pvgis_df_period_grp)




















