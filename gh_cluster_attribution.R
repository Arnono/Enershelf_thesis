

#General script for the extraction of:
#Admin attributes 
#Polygon areas
#Polygon population


#Read required Libraries
library(sf)

setwd("C:\\rli\\ghana_project")
datapath<-("C:\\rli\\ghana_project")

nga_adm1_sf <- st_read(file.path(datapath,"source_data\\01_Administrative_Boundaries\\GHA_admbndp1_1m_GAUL.shp"))%>% 
  st_transform(32630) 
nga_adm2_sf <- st_read(file.path(datapath,"source_data\\01_Administrative_Boundaries\\GHA_admbndp2_1m_GAUL.shp"))%>% 
  st_transform(32630)
pop_clusters_sf <- st_read(file.path(datapath,"source_data\\cluster_processes\\gh_join_clust_32630_gh_health_facilities_32630.shp"))%>% 
  st_transform(32630) 

######
##Main workflow


#Calculate the centroids

clust_cent_sf <- st_centroid(pop_clusters_sf)
#cent_coordinates <- st_coordinates(clust_cent_sf)

#x_cent <- cent_coordinates[c(TRUE, FALSE)]
#y_cent <- cent_coordinates[c(FALSE, TRUE)]

#Add adnim 1 and 2 columns
cent_adm1 <- st_join(clust_cent_sf, left = TRUE, nga_adm1_sf["ADM1_NAME"])
cent_adm2 <- st_join(clust_cent_sf, left = TRUE, nga_adm2_sf["ADM2_NAME"])
cent_adm1_pcod <- st_join(clust_cent_sf, left = TRUE, nga_adm1_sf["ADM1_CODE"])
cent_adm2_pcod <- st_join(clust_cent_sf, left = TRUE, nga_adm2_sf["ADM2_CODE"])
#pcoded aptation 

#Convert data to a projected coordinate system (UTM zone 32N)
pop_clusters_crs_32630 <- st_transform(pop_clusters_sf, 32630)

#Calculate areas and add to attribute table (Square KM)
clust_area <- (st_area(pop_clusters_crs_32630))/1000000
areas <- as.double(as.array(clust_area))


#pipe data to dataframe
pop_clusters_crs_32630$admin1 <- cent_adm1$ADM1_NAME
pop_clusters_crs_32630$admin2 <- cent_adm2$ADM2_NAME
pop_clusters_crs_32630$admin1Pcod <- cent_adm1_pcod$ADM1_CODE
pop_clusters_crs_32630$admin2Pcod <- cent_adm2_pcod$ADM2_CODE
pop_clusters_crs_32630$area_km2 <- areas
#pop_clusters_crs_32632$x_cent <- x_cent
#pop_clusters_crs_32632$y_cent <- y_cent


#reproject to EPSG 4326 and write to file
pop_clusters_4326 <- st_transform(pop_clusters_crs_32630, 4326) %>% st_as_sf()




#Write to file
#datapath_write <- ("//srv02/RL-Institut/04_Projekte/240_NESP2/09-Stud_Ordner/Arnold/results/unsorted")
#st_write(pop_clusters_sf, file.path(datapath_write,"nigeria_cluster_attributes.shp"))


########################################################################################


#General script for the extraction of:
#Population properties from raster layer
#HRSL


#Read required Libraries
library(raster)
require(exactextractr)

#Read files
pop_clusters_sf <- pop_clusters_4326
hrsl_population_rast <- raster(file.path(datapath,"source_data\\02_population\\stretched\\population_gha_2018-10-01.tif"))

Sys.time()
sum_rast <- exact_extract(hrsl_population_rast, pop_clusters_sf,'sum')
Sys.time()

pop_clusters_sf$pop_hV2 <- sum_rast

st_write(pop_clusters_sf,"r_results\\gh_clust_mergedV1V2_attributed_v1.shp")


#Voronoi poly attribution

gh_hosp_vor <- st_read("test_res\\hosp_voronoi_polygons.shp") %>% 
  st_transform(4326) 
hrsl_population_rast <- raster(file.path(datapath,"source_data\\02_population\\stretched\\population_gha_2018-10-01.tif"))

Sys.time()
sum_rast <- exact_extract(hrsl_population_rast, gh_hosp_vor,'sum')
Sys.time()

gh_hosp_vor$loco_pop <- sum_rast

st_write(gh_hosp_vor,"r_results\\gh_hosp_voronoi_pop.shp")



#Jan 2021
#Add 2020 population
#Read required Libraries
library(raster)
require(exactextractr)

#Read files
pop_clusters_sf <- st_read(file.path(datapath,"r_results\\gh_clust_mergedV1V2_attributed_v1.shp"))
hrsl_population_rast <- raster(file.path(datapath,"source_data\\02_population\\population_gha_2021-01-09_4326_stretched.tif"))
dlr_population_rast <- raster(file.path(datapath,"source_data\\02_population\\GUF_dlr\\derivatives\\gh_2020_buildings_rast_pop_4326_str.tif"))

Sys.time()
sum_rastH <- exact_extract(hrsl_population_rast, pop_clusters_sf,'sum')
sum_rastD <- exact_extract(dlr_population_rast, pop_clusters_sf,'sum')
Sys.time()

pop_clusters_sf$popH_2020 <- sum_rastH
pop_clusters_sf$popD_2020 <- sum_rastD

st_write(pop_clusters_sf,"r_results\\gh_clust_mergedV1V2_attributed_v2.shp")
s


#get point coordinates
sim_points <- st_read(file.path(datapath,"mg_sims\\hospitals\\sim_hospitals.shp"))

hosp_coords <- st_coordinates(sim_points) %>% as.data.frame()

sim_points$x_cent <- hosp_coords$X
sim_points$y_cent <- hosp_coords$Y

st_write(sim_points,"mg_sims\\hospitals\\sim_hospitals_coords_2.shp")



