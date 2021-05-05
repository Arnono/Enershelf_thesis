# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 19:47:50 2021

@author: arnow
"""


# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 17:47:10 2020

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
i=2

pvgis_url = "https://re.jrc.ec.europa.eu/api/seriescalc"


wind_pt =pd.DataFrame(np.zeros(8760))

#Iterate over Locations
for i in range(0,len(df_dailydemand)):
        print(i)
        #Pull pvgis data online
        latitude = (df_dailydemand.iloc[i,4])
        longitude = (df_dailydemand.iloc[i,5])
        args = {
            'lat': latitude,
            'lon': longitude,
            'startyear': 2014,
            'endyear': 2014,
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
        slr_pt = pvgis_data["P"]
        
               
        #create lp_lists of tier2       
        ds_lp_day=(ds_lp_percent*df_dailydemand.iloc[i,1])
        ds_lp_year=pd.concat([ds_lp_day]*365)
        
        df_feat_tier_2 = pd.DataFrame(ds_lp_year)
        df_feat_tier_2 = df_feat_tier_2.rename(columns={'percentage per hour ': 'Demand'})
        df_feat_tier_2["SolarGen"] = slr_pt
        df_feat_tier_2["Wind"] = wind_pt #Demand;SolarGen;Wind
        f_name = "tier_2\\gh_site_" + str(df_dailydemand.iloc[i,0])+".csv"
        df_feat_tier_2.to_csv(f_name, index=False,sep=";")
        
        
        list_lp_tier_2.append(ds_lp_year.reset_index(drop=True))
        
        #create lp_lists of tier3
        ds_lp_day=(ds_lp_percent*df_dailydemand.iloc[i,2])
        ds_lp_year=pd.concat([ds_lp_day]*365)
        list_lp_tier_3.append(ds_lp_year.reset_index(drop=True))
        
        #create lp_lists of tier4
        ds_lp_day=(ds_lp_percent*df_dailydemand.iloc[i,3])
        ds_lp_year=pd.concat([ds_lp_day]*365)
        list_lp_tier_4.append(ds_lp_year.reset_index(drop=True))
        
        

df_tier_2=pd.DataFrame(list_lp_tier_2,index=fid_list)
df_tier_3=pd.DataFrame(list_lp_tier_3,index=fid_list)
df_tier_4=pd.DataFrame(list_lp_tier_4,index=fid_list)
df_tier_2=df_tier_2.transpose()
df_tier_2=df_tier_3.transpose()
df_tier_4=df_tier_4.transpose()

df_tier_2.to_csv("loadprofiles_tier_2_gh_2020.csv", index=False)
df_tier_3.to_csv("loadprofiles_tier_3_gh_2020.csv", index=False)
df_tier_4.to_csv("loadprofiles_tier_4_gh_2020.csv", index=False)

df_tier_4.shape

list_lp_tier_2.shape

#write individual sim csvs









