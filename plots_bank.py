# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 15:27:22 2021

@author: arnow
"""
# library & dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


df = sns.load_dataset('iris')
 
# with regression
sns.pairplot(df, kind="reg")
plt.show()
 
# without regression
sns.pairplot(df, kind="scatter")
plt.show()

sns.pairplot(df, kind="scatter", hue="species", markers=["o", "s", "D"], palette="Set2")
plt.show()

sns.pairplot(df, hue="species")
plt.show()
 
# right: you can give other arguments with plot_kws.
sns.pairplot(df, kind="scatter", hue="species", plot_kws=dict(s=80, edgecolor="white", linewidth=2.5))
plt.show()





###
os.chdir('C:\\rli\\ghana_project\\data_2_hist')

#001 - Distance to grid
data_in = pd.read_csv('hosp_gdist_data.csv')

sns.set_theme()

fig,axs = plt.subplots(figsize=(10,10) ) 
plt.hist(data_in.distance,20,color="#3b85d3ff")
plt.yscale('log', nonposy='clip')
plt.xlabel("Distance (M)")
plt.ylabel("Frequency")


#002 - Night lihght
data_in = pd.read_csv('gh_night_light_data.csv')

fig,axs = plt.subplots(figsize=(10,10) ) 
plt.hist(data_in.DN,20,color="#3b85d3ff")
plt.yscale('log', nonposy='clip')
plt.xlabel("DN Value")
plt.ylabel("Frequency")

fig,axs = plt.subplots(figsize=(10,10) ) 
plt.hist(data_in.DN[data_in.DN < 100],20,color="#3b85d3ff")
plt.yscale('log', nonposy='clip')
plt.xlabel("DN Value")
plt.ylabel("Frequency")

#003
data_in = pd.read_csv('vor_dens_pop_hosp_area_data.csv')

fig,axs = plt.subplots(figsize=(10,10) ) 
plt.hist(data_in.den_p_h_km,20,color="#3b85d3ff")
plt.yscale('log', nonposy='clip')
plt.xlabel("Population per Hospital per Square KM")
plt.ylabel("Frequency")


#003
data_in = pd.read_csv('dist_dens_pop_hosp_area_data.csv')

fig,axs = plt.subplots(figsize=(10,10) ) 
plt.hist(data_in.den_p_h_km,20,color="#3b85d3ff")
plt.yscale('log', nonposy='clip')
plt.xlabel("Population per Hospital per Square KM")
plt.ylabel("Frequency")


#003
data_in = pd.read_csv('gh_pop_per_hosp_hist.csv')

fig,axs = plt.subplots(figsize=(10,10) ) 
plt.hist(data_in.vj_pop_hos,20,color="#3b85d3ff")
plt.yscale('log', nonposy='clip')
plt.xlabel("Population per Hospital")
plt.ylabel("Frequency")

#003
data_in = pd.read_csv('gh_pop_per_hosp_hist.csv')

fig,axs = plt.subplots(figsize=(10,10) ) 
plt.hist(data_in.vj_pop_hos[data_in.vj_pop_hos < 10000],10,color="#3b85d3ff")
plt.yscale('log', nonposy='clip')
plt.xlabel("Population per Hospital")
plt.ylabel("Frequency")




data_in = pd.read_csv('gh_auto_clust_properties.csv')

fig,axs = plt.subplots(figsize=(10,10) ) 
plt.hist(data_in.area_km2,20,color="#3b85d3ff")
plt.yscale('log', nonposy='clip')
plt.xlabel("Cluster area")
plt.ylabel("Frequency")

fig,axs = plt.subplots(figsize=(10,10) ) 
plt.hist(data_in.area_km2[data_in.area_km2 > 0.8][data_in.area_km2 < 2],20,color="#3b85d3ff")
#plt.yscale('log', nonposy='clip')
plt.xlabel("Cluster area")
plt.ylabel("Frequency")

fig,axs = plt.subplots(figsize=(10,10) ) 
plt.hist(data_in.pop_hV2[data_in.area_km2 > 0.8][data_in.area_km2 < 2],20,color="#3b85d3ff")
plt.yscale('log', nonposy='clip')
plt.xlabel("Population")
plt.ylabel("Frequency")

fig,axs = plt.subplots(figsize=(10,10) ) 
plt.hist(data_in.popH_2020[data_in.area_km2 > 0.8][data_in.area_km2 < 2],20,color="#3b85d3ff")
plt.yscale('log', nonposy='clip')
plt.xlabel("Population")
plt.ylabel("Frequency")

fig,axs = plt.subplots(figsize=(10,10) ) 
plt.hist(data_in.pop_den,20,color="#3b85d3ff")
plt.yscale('log', nonposy='clip')
plt.xlabel("Population density")
plt.ylabel("Frequency")


#Daily Load profile 
os.chdir('C:\\rli\\ghana_project\\mg_sims')
df_lp_percent=pd.read_excel('loadprofile_percentages_gh.xlsx')

ig, axs = plt.subplots(figsize=(10,6))
plt.bar(list(df_lp_percent.index.values),df_lp_percent["percentage per hour "])
plt.xlabel("Time in hours",fontsize=16)  # custom x label using matplotlib
plt.ylabel("Percentage Consumption",fontsize=16)


#Tiers demand viz
os.chdir('C:\\rli\\ghana_project\\mg_sims')
df_daily_dem = pd.read_excel('daily_demand_clusters_2020_gh_to_plot.xlsx')

ig, axs = plt.subplots(figsize=(10,6))
plt.plot(list(df_daily_dem.index.values),df_daily_dem["daily_demand_tier2 (Wh)"],linewidth=3.0, label='Tier 2')
plt.plot(list(df_daily_dem.index.values),df_daily_dem["daily_demand_tier3 (Wh)"],linewidth=3.0, label='Tier 3')
plt.plot(list(df_daily_dem.index.values),df_daily_dem["daily_demand_tier4 (Wh)"],linewidth=3.0, label='Tier 4')
plt.legend(frameon=False)
plt.xlabel("Clusters",fontsize=16)
plt.ylabel("Daily Consumption (KWh)",fontsize=16)


#Tiers results viz
os.chdir('C:\\rli\\ghana_project\\mg_sims\\results_viz')
#df_tier_og_res = pd.read_excel('og_tiers_res_plot.xlsx')
df_tier_og_res = pd.read_csv('og_tiers_res_plot_2.csv')

ig, axs = plt.subplots(figsize=(10,6))
plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t2_FI_PS"],linewidth=3.0, label='Tier 2 PS')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t3_FI_PS"],linewidth=3.0, label='Tier 3 PS')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t4_FI_PS"],linewidth=3.0, label='Tier 4 PS')
plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t2_FI_PDS"],linewidth=3.0, label='Tier 2 PDS')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t3_FI_PDS"],linewidth=3.0, label='Tier 3 PDS')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t4_FI_PDS"],linewidth=3.0, label='Tier 4 PDS')
plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["tH_FI_PS"],linewidth=3.0, label='Hospital PS')
plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["tH_FI_PDS"],linewidth=3.0, label='Hospital PDS')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t2_FI_ninja_PS"],linewidth=3.0, label='Tier 2 PS NJ')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t3_FI_ninja_PS"],linewidth=3.0, label='Tier 3 PS NJ')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t4_FI_ninja_PS"],linewidth=3.0, label='Tier 4 PS NJ')
# plt.yscale('log', nonposy='clip')
plt.legend(frameon=False)
plt.xlabel("Clusters",fontsize=16)
plt.ylabel("First Investment ($)",fontsize=16)



ig, axs = plt.subplots(figsize=(10,6))
#Differences
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t3_FI_PS"]-df_tier_og_res["t3_FI_PDS"],linewidth=3.0, label='Tier 3 PS-PDS')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t4_FI_PS"]-df_tier_og_res["t4_FI_PDS"],linewidth=3.0, label='Tier 4 PS-PDS')
#Percentages
plt.plot(list(df_tier_og_res.index.values),(df_tier_og_res["tH_FI_PS"]/df_tier_og_res["t2_FI_PS"])*100,linewidth=3.0, label='Hosp% of T2 PS')
plt.plot(list(df_tier_og_res.index.values),(df_tier_og_res["tH_FI_PDS"]/df_tier_og_res["t2_FI_PDS"])*100,linewidth=3.0, label='Hosp% of T2 PDS')
#plt.yscale('log', nonposy='clip')
plt.legend(frameon=False)
plt.xlabel("Clusters",fontsize=16)
plt.ylabel("Percentage of FI",fontsize=16)


#Explore
np.mean(df_tier_og_res["tH_FI_PS"])
(max(df_tier_og_res["tH_FI_PS"])- min(df_tier_og_res["tH_FI_PS"])) / np.mean(df_tier_og_res["tH_FI_PS"])

np.mean(df_tier_og_res["t2_FI_PS"])
np.mean(df_tier_og_res["t2_FI_ninja_PS"])

sum(df_tier_og_res["t2_FI_PS"]) - sum(df_tier_og_res["t2_FI_ninja_PS"])
sum(df_tier_og_res["t2_FI_ninja_PS"])

sum(df_tier_og_res["t2_FI_PS"])/28000000000

#Mean errors
(np.mean(df_tier_og_res["t2_FI_PS"])-np.mean(df_tier_og_res["t2_FI_ninja_PS"]))/np.mean(df_tier_og_res["t2_FI_PS"])
(np.mean(df_tier_og_res["t3_FI_PS"])-np.mean(df_tier_og_res["t3_FI_ninja_PS"]))/np.mean(df_tier_og_res["t3_FI_PS"])
(np.mean(df_tier_og_res["t4_FI_PS"])-np.mean(df_tier_og_res["t4_FI_ninja_PS"]))/np.mean(df_tier_og_res["t4_FI_PS"])

np.mean(abs(df_tier_og_res["t2_FI_PS"]-df_tier_og_res["t2_FI_ninja_PS"])/df_tier_og_res["t2_FI_PS"]*100)




#Percentage difference to NINJA
ig, axs = plt.subplots(figsize=(10,6))
plt.bar(list(df_tier_og_res.index.values),((df_tier_og_res["t2_FI_PS"]-df_tier_og_res["t2_FI_ninja_PS"])/df_tier_og_res["t2_FI_PS"])*100,linewidth=3.0, label='Hosp% of T2 PDS')
plt.xlabel("Clusters",fontsize=16)
plt.ylabel("% Diff to Ninja",fontsize=16)

ig, axs = plt.subplots(figsize=(10,6))
plt.hist(((df_tier_og_res["t2_FI_PS"]-df_tier_og_res["t2_FI_ninja_PS"])/df_tier_og_res["t2_FI_PS"])*100,20)
plt.xlabel("% Diff to Ninja",fontsize=16)
plt.ylabel("Frequency",fontsize=16)


#Error bar
ig, axs = plt.subplots(figsize=(10,6))
# plt.yscale('log', nonposy='clip')
plt.errorbar(list(df_tier_og_res.index.values),df_tier_og_res["t2_FI_PS"],yerr= (abs(df_tier_og_res["t2_FI_PS"]-df_tier_og_res["t2_FI_ninja_PS"])),fmt='o', markersize=2, capsize=3)
plt.xlabel("Clusters",fontsize=16)
plt.ylabel("First Investment ($)",fontsize=16)




# =============================================================================
# LCOEs
# =============================================================================

ig, axs = plt.subplots(figsize=(10,6))
plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t2_lcoe_PS"],linewidth=2.0, label='Tier 2 PS')
plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t3_lcoe_PS"],linewidth=2.0, label='Tier 3 PS')
plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t4_lcoe_PS"],linewidth=2.0, label='Tier 4 PS')
plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t2_lcoe_PDS"],linewidth=2.0, label='Tier 2 PDS')
plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t3_lcoe_PDS"],linewidth=2.0, label='Tier 3 PDS')
plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t4_lcoe_PDS"],linewidth=2.0, label='Tier 4 PDS')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["th_lcoe_PS"],linewidth=2.0, label='Hospital PS')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["th_lcoe_PDS"],linewidth=2.0, label='Hospital PDS')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t2_lcoe_PS_nj"],linewidth=2.0, label='Tier 2 PS NJ')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t3_lcoe_PS_nj"],linewidth=2.0, label='Tier 3 PS NJ')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t4_lcoe_PS_nj"],linewidth=2.0, label='Tier 4 PS NJ')
# plt.yscale('log', nonposy='clip')
plt.ylim((0.2,0.7))
plt.legend(frameon=False)
plt.xlabel("Clusters",fontsize=16)
plt.ylabel("LCOE ($)",fontsize=16)



ig, axs = plt.subplots(figsize=(10,6))
#Differences
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t3_FI_PS"]-df_tier_og_res["t3_FI_PDS"],linewidth=3.0, label='Tier 3 PS-PDS')
# plt.plot(list(df_tier_og_res.index.values),df_tier_og_res["t4_FI_PS"]-df_tier_og_res["t4_FI_PDS"],linewidth=3.0, label='Tier 4 PS-PDS')
#Percentages
plt.plot(list(df_tier_og_res.index.values),(df_tier_og_res["th_lcoe_PS"]/df_tier_og_res["t2_lcoe_PS"])*100,linewidth=3.0, label='Hosp% of T2 PS')
plt.plot(list(df_tier_og_res.index.values),(df_tier_og_res["th_lcoe_PDS"]/df_tier_og_res["t2_lcoe_PDS"])*100,linewidth=3.0, label='Hosp% of T2 PDS')
#plt.yscale('log', nonposy='clip')
plt.legend(frameon=False)
plt.xlabel("Clusters",fontsize=16)
plt.ylabel("Percentage of LCOE",fontsize=16)


#Explore
np.mean(df_tier_og_res["tH_FI_PS"])
(max(df_tier_og_res["tH_FI_PS"])- min(df_tier_og_res["tH_FI_PS"])) / np.mean(df_tier_og_res["tH_FI_PS"])

np.mean(df_tier_og_res["t2_FI_PS"])
np.mean(df_tier_og_res["t2_FI_ninja_PS"])

sum(df_tier_og_res["t2_FI_PS"]) - sum(df_tier_og_res["t2_FI_ninja_PS"])
sum(df_tier_og_res["t2_FI_ninja_PS"])

sum(df_tier_og_res["t2_FI_PS"])/28000000000

#Mean errors
(np.mean(df_tier_og_res["t2_FI_PS"])-np.mean(df_tier_og_res["t2_FI_ninja_PS"]))/np.mean(df_tier_og_res["t2_FI_PS"])
(np.mean(df_tier_og_res["t3_FI_PS"])-np.mean(df_tier_og_res["t3_FI_ninja_PS"]))/np.mean(df_tier_og_res["t3_FI_PS"])
(np.mean(df_tier_og_res["t4_FI_PS"])-np.mean(df_tier_og_res["t4_FI_ninja_PS"]))/np.mean(df_tier_og_res["t4_FI_PS"])

np.mean(abs(df_tier_og_res["t2_FI_PS"]-df_tier_og_res["t2_FI_ninja_PS"])/df_tier_og_res["t2_FI_PS"]*100)




#Percentage difference to NINJA
ig, axs = plt.subplots(figsize=(10,6))
plt.bar(list(df_tier_og_res.index.values),((df_tier_og_res["t2_lcoe_PS"]-df_tier_og_res["t2_lcoe_PS_nj"])/df_tier_og_res["t2_lcoe_PS"])*100,linewidth=3.0, label='Hosp% of T2 PDS')
plt.xlabel("Clusters",fontsize=16)
plt.ylabel("% Diff to Ninja LCOE",fontsize=16)

ig, axs = plt.subplots(figsize=(10,6))
plt.hist(((df_tier_og_res["t2_lcoe_PS"]-df_tier_og_res["t2_lcoe_PS_nj"])/df_tier_og_res["t2_lcoe_PS"])*100,20)
plt.xlabel("% Diff to Ninja LCOE",fontsize=16)
plt.ylabel("Frequency",fontsize=16)


#Error bar
ig, axs = plt.subplots(figsize=(10,6))
# plt.yscale('log', nonposy='clip')
plt.errorbar(list(df_tier_og_res.index.values),df_tier_og_res["t2_lcoe_PS"],yerr= (abs(df_tier_og_res["t2_lcoe_PS"]-df_tier_og_res["t2_lcoe_PS_nj"])),fmt='o', markersize=2, capsize=3)
plt.xlabel("Clusters",fontsize=16)
plt.ylabel("LCOE ($)",fontsize=16)

































#Locations and demand profiles Import 
df_dailydemand=pd.read_excel('daily_demand_clusters_2020_gh.xlsx')
df_lp_percent=pd.read_excel('loadprofile_percentages_gh.xlsx')
ds_lp_percent=df_lp_percent.iloc[:,0]
df_dailydemand.head()

df_dailydemand=df_dailydemand.rename(columns={'feature_id': 'fid', 'daily_demand_tier2 (Wh)':'tier_2','daily_demand_tier3 (Wh)':'tier_3','daily_demand_tier4 (Wh)':'tier_4'})


plt.hist(df_dailydemand.tier_2,15)

sns.set_theme()
sns.displot(df_dailydemand.tier_2,bins=15)


fig,axs = plt.subplots(figsize=(12.8,7.2) ) 
plt.hist(df_dailydemand.tier_2,10)
plt.bar(df_dailydemand.index,df_dailydemand.tier_2)









































