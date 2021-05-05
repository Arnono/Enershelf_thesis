


library(raster)
library(sf)
library(sp)
library(rgdal)
library(rgeos)
library(dbscan)
library(dplyr)
library(ggplot2)
library(mapview)
library(tmap)
library(geosphere)
library(leaflet)
setwd("C:\\rli\\ghana_project")

datapath<-("C:\\rli\\ghana_project")
#builtup<-raster(file.path(datapath,"source_data\\02_population\\hrsl_gha_pop.tif"))
builtup<-raster(file.path(datapath,"source_data\\02_population\\GUF_dlr\\derivatives\\gh_2020_buildings_rast_pop_4326.tif"))

adm1<-st_read(file.path(datapath,"source_data\\01_Administrative_Boundaries\\GHA_admbndp1_1m_GAUL.shp"))
adm1 %>% select(ADM1_NAME) %>% ggplot() + geom_sf() + labs(title = "Ghana")




Sys.time()
Kano<- adm1
builtup_Kano<-crop(builtup,Kano) #crop clips the data to the given extent
builtup_Kano<-mask(builtup_Kano,Kano) #mask excludes data inside the extent but outside the specified shape
#transform raster centerpoints to points


#pts_buildup_Kano<-rasterToPoints(builtup_Kano, spatial=TRUE)
pts_buildup_Kano<-rasterToPoints(builtup, spatial=TRUE)
summary_Kano <-summary(pts_buildup_Kano)

#pix_points <-st_read(file.path(datapath,"source_data\\02_population\\GUF_dlr\\derivatives\\gh_pix_point_vect_joined.shp"))
#input=as.data.frame.array(pix_points@coords)

input=as.data.frame.array(pts_buildup_Kano@coords)




test=dbscan(input, eps = 0.00083, minPts = 5, weights = NULL)
options(max.print = 3)
print(test)
input$cluster <- test$cluster
#split the original data into two according to whether dbscan has assigned or cluster or noise.
groups  <- input %>% filter(cluster != 0)
noise  <- input %>% filter(cluster== 0)
out <- input %>% 
  st_as_sf(coords = c("x","y"), crs = 4326) %>%
  group_by(cluster) %>% 
  summarise() %>% 
  st_convex_hull()

out %>% filter(cluster == 0) 
outfiltered <- out %>% filter(cluster != 0)
union <- st_union(outfiltered,by_feature = FALSE)
union_poly <- st_collection_extract(
  union,
  type = c("POLYGON"),
  warn = FALSE
)

st_write(union_poly, "gh_pop_cluster_dlr_gsl.shp")
Sys.time()











