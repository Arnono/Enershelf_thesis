# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:17:37 2021

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
import json



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



token = '9a0117c2c0f94bc1d058d93d3ecbc704ab557b6f'
api_base = 'https://www.renewables.ninja/api/'

s = requests.session()
s.headers = {'Authorization': 'Token ' + token}

url = api_base + 'data/pv'
wind_pt =pd.DataFrame(np.zeros(8760))


#Iterate over Locations
for i in range(0,len(df_dailydemand)):
        print(i)
        #Pull pvgis data online
        latitude = (df_dailydemand.iloc[i,5])
        longitude = (df_dailydemand.iloc[i,4])
        args = {
            'lat': latitude,
            'lon': longitude,
            'date_from': '2015-01-01',
            'date_to': '2015-12-31',
            'dataset': 'merra2',
            'capacity': 1.0,
            'system_loss': 0.1,
            'tracking': 0, 
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
        slr_pt = data["electricity_si"]
        slr_pt.reset_index(drop=True, inplace=True)
        #sum(slr_pt)
               
        #create lp_lists of tier2       
        ds_lp_day=(ds_lp_percent/100*df_dailydemand.iloc[i,1])
        ds_lp_year=pd.concat([ds_lp_day]*365)
        
        df_feat_tier_2 = pd.DataFrame(ds_lp_year)
        df_feat_tier_2 = df_feat_tier_2.rename(columns={'percentage per hour ': 'Demand'})
        df_feat_tier_2["SolarGen"] = slr_pt/1000
        df_feat_tier_2["Wind"] = wind_pt #Demand;SolarGen;Wind
        f_name = "tier_2_ninja\\gh_site_" + str(df_dailydemand.iloc[i,0])+".csv"
        df_feat_tier_2.to_csv(f_name, index=False,sep=";")
        
        
        #create lp_lists of tier3
        ds_lp_day=(ds_lp_percent/100*df_dailydemand.iloc[i,2])
        ds_lp_year=pd.concat([ds_lp_day]*365)
        
        df_feat_tier_3 = pd.DataFrame(ds_lp_year)
        df_feat_tier_3 = df_feat_tier_3.rename(columns={'percentage per hour ': 'Demand'})
        df_feat_tier_3["SolarGen"] = slr_pt/1000
        df_feat_tier_3["Wind"] = wind_pt #Demand;SolarGen;Wind
        f_name = "tier_3_ninja\\gh_site_" + str(df_dailydemand.iloc[i,0])+".csv"
        df_feat_tier_3.to_csv(f_name, index=False,sep=";")
        
        
        #create lp_lists of tier4
        ds_lp_day=(ds_lp_percent/100*df_dailydemand.iloc[i,3])
        ds_lp_year=pd.concat([ds_lp_day]*365)
        
        df_feat_tier_4 = pd.DataFrame(ds_lp_year)
        df_feat_tier_4 = df_feat_tier_4.rename(columns={'percentage per hour ': 'Demand'})
        df_feat_tier_4["SolarGen"] = slr_pt/1000
        df_feat_tier_4["Wind"] = wind_pt #Demand;SolarGen;Wind
        f_name = "tier_4_ninja\\gh_site_" + str(df_dailydemand.iloc[i,0])+".csv"
        df_feat_tier_4.to_csv(f_name, index=False,sep=";")
        print("pause ")
        time.sleep(75)
        
        





















