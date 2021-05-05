# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 12:40:21 2021

@author: arnow
"""
import pandas as pd
import numpy as np
#import cdsapi
import xarray as xr
from pandas import ExcelWriter
from pandas import ExcelFile
import os
import requests
import time

from pvlib import location
from pvlib import irradiance
from scipy import stats



os.chdir('C:\\rli\\ghana_project\\mg_sims')

#Locations and demand profiles Import 
df_dailydemand=pd.read_excel('daily_demand_clusters_2020_gh.xlsx')
df_lp_percent=pd.read_excel('loadprofile_percentages_gh.xlsx')
ds_lp_percent=df_lp_percent.iloc[:,0]
df_dailydemand.head()

df_dailydemand=df_dailydemand.rename(columns={'feature_id': 'fid', 'daily_demand_tier2 (Wh)':'tier_2','daily_demand_tier3 (Wh)':'tier_3','daily_demand_tier4 (Wh)':'tier_4'})
df_dailydemand.tier_2=df_dailydemand.tier_2[:]/1000
df_dailydemand.tier_3=df_dailydemand.tier_3[:]/1000
df_dailydemand.tier_4=df_dailydemand.tier_4[:]/1000
df_dailydemand.head()

fid_list=[df_dailydemand.fid]
list_lp_tier_2=[]
list_lp_tier_3=[]
list_lp_tier_4=[]

pv_pot_pvgis=[]

pvgis_url = "https://re.jrc.ec.europa.eu/api/seriescalc"


wind_pt =pd.DataFrame(np.zeros(8760))

#Iterate over Locations
for i in range(0,len(df_dailydemand)): #len(df_dailydemand)
        print(i)
        #Pull pvgis data online
        latitude = (df_dailydemand.iloc[i,5])
        longitude = (df_dailydemand.iloc[i,4])
        args = {
            'lat': latitude,
            'lon': longitude,
            'startyear': 2015,
            'endyear': 2015,
            'outputformat':'json',
            'pvcalculation':1,
            'peakpower':1,
            'loss':10 
        }
        
        pvgis_get = requests.get(pvgis_url, params = args)
        pvgis_parsed_response = pvgis_get.json()
        
        inputs = pvgis_parsed_response['inputs']
        meta = pvgis_parsed_response['meta']
        hourly_data = pvgis_parsed_response['outputs']['hourly']
        pvgis_data = pd.DataFrame(hourly_data)
        slr_pt = pvgis_data["P"]
          
        pvgis_data["time"] = pd.to_datetime(pvgis_data['time'], format='%Y%m%d:%H%M', utc=True)
        pvgis_df_period_grp = pvgis_data.groupby(pvgis_data["time"].dt.week)["P"].mean()
        
        pv_pot_pvgis.append(pvgis_df_period_grp)
        
        


      
pv_array = pd.DataFrame(pv_pot_pvgis,index= df_dailydemand["fid"])            
pv_array = pv_array.transpose()       
pv_array.to_csv("weekly_pv_potential_weekC.csv")        
    
        
        
# =============================================================================
#         
# Clear sky data               
# =============================================================================
        

tz = 'Africa/Accra'

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



os.chdir('C:\\rli\\ghana_project\\mg_sims')

#Locations and demand profiles Import 
df_dailydemand=pd.read_excel('daily_demand_clusters_2020_gh.xlsx')
df_lp_percent=pd.read_excel('loadprofile_percentages_gh.xlsx')
ds_lp_percent=df_lp_percent.iloc[:,0]
df_dailydemand.head()

df_dailydemand=df_dailydemand.rename(columns={'feature_id': 'fid', 'daily_demand_tier2 (Wh)':'tier_2','daily_demand_tier3 (Wh)':'tier_3','daily_demand_tier4 (Wh)':'tier_4'})
df_dailydemand.tier_2=df_dailydemand.tier_2[:]/1000
df_dailydemand.tier_3=df_dailydemand.tier_3[:]/1000
df_dailydemand.tier_4=df_dailydemand.tier_4[:]/1000
df_dailydemand.head()

fid_list=[df_dailydemand.fid]


pv_clr_sky=[]



#Iterate over Locations
for i in range(0,len(df_dailydemand)): #len(df_dailydemand)
        print(i)
        #Pull pvgis data online
        latitude = (df_dailydemand.iloc[i,5])
        longitude = (df_dailydemand.iloc[i,4])
        
        lat, lon = latitude, longitude
        site = location.Location(lat, lon, tz=tz)
        
        pvlib_sim_clear = get_irradiance(site, 30, 180)
        pvlib_sim_clear["time"] = list(pvlib_sim_clear.index.values)
        
        pvlib_sim_clear_weekly = pvlib_sim_clear.groupby(pvlib_sim_clear["time"].dt.week)["GHI"].mean()      
        pv_clr_sky.append(pvlib_sim_clear_weekly)
        
        


      
pv_cl_array = pd.DataFrame(pv_clr_sky,index= df_dailydemand["fid"])            
#pv_cl_array = pv_cl_array.transpose()       
pv_cl_array.to_csv("weekly_pv_clrsky_potential_weekC.csv")           
        
        
        
        
        
































