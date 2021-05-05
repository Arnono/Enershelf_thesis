

library(sf)
library(raster)
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

admin_1 <- st_read(file.path(datapath,"source_data\\01_Administrative_Boundaries\\GHA_admbndp1_1m_GAUL.shp"))%>% 
  st_transform(32630) 
cv1 <- st_read(file.path(datapath,"gh_pop_cluster_hrsl_v1.shp"))%>% 
  st_transform(32630) 
cv2 <- st_read(file.path(datapath,"gh_pop_cluster_hrsl_v2.shp"))%>% 
  st_transform(32630) 

admin_list <- admin_1$ADM1_NAME

#admin_list <- admin_list[c(1,2,4)]
#admin_list <- admin_list[14]
#states_to_get <- c(4,11,14)

counter <- 0

for (i in admin_list){
  counter = counter + 1
  print(i)
  print(counter)
  print('start cycle')
  admin_select <- admin_1 %>% filter(ADM1_NAME == i)
  
  #Extract V1
  cv1_x     <- st_intersects(admin_select,cv1, sparse = F) %>%  t() %>% as.array()
  cv1$ints  <- cv1_x
  cv1_xtract<- cv1 %>% filter(ints == TRUE) %>% st_buffer(10)
  cv1$ints  <- NULL
  
  #Extract V2
  cv2_x     <- st_intersects(admin_select,cv2, sparse = F) %>%  t() %>% as.array()
  cv2$ints  <- cv2_x
  cv2_xtract<- cv2 %>% filter(ints == TRUE) %>% st_buffer(10)
  cv2$ints  <- NULL
  
  v1_merge  <- st_union(cv1_xtract) %>% st_cast('POLYGON') %>% st_combine() %>% st_as_sf()
  v2_merge  <- st_union(cv2_xtract) %>% st_cast('POLYGON') %>% st_combine() %>% st_as_sf()
  
  print("Union")
  Sys.time() %>% print
  v1v2 <- st_union(v1_merge,v2_merge)
  Sys.time() %>% print
  
  unmarked_v1v2 <- v1v2 %>% st_cast('POLYGON') %>% 
    as.data.frame() %>% st_as_sf() %>% st_buffer(-10)
  
  if (!exists("mega_join_clust")){
    mega_join_clust <- unmarked_v1v2
  }else {
    mega_join_clust <- rbind(mega_join_clust,unmarked_v1v2)
  }
  
  remove(cv1_xtract,cv1_x,cv2_xtract,cv2_x,v1v2,v1_merge,v2_merge,unmarked_v1v2)
  print('End cycle')
  Sys.time() %>% print
}

counter <- 0

for (i in admin_list){
  counter = counter + 1
  print(i)
  print(counter)
  print('start cycle 2')
  admin_select <- admin_1 %>% filter(ADM1_NAME == i)
  
  #Extract union admin
  union_x      <- st_intersects(admin_select,mega_join_clust, sparse = F) %>%  t() %>% as.array()
  mega_join_clust$ints  <- union_x
  union_xtract <- mega_join_clust %>% filter(ints == TRUE) 
  mega_join_clust$ints  <- NULL
  
  #Extract union 
  clst_adm_sel <- union_xtract %>% st_union()
  union_xx       <- st_intersects(clst_adm_sel,mega_join_clust, sparse = F) %>%  t() %>% as.array()
  mega_join_clust$ints2  <- union_xx
  union_xtract_x <- mega_join_clust %>% filter(ints2 == TRUE)
  mega_join_clust$ints2  <- NULL
  

  union_merge  <- st_union(union_xtract_x) %>% st_cast('POLYGON') %>% 
    st_combine() %>% st_as_sf()
  remerge_v1v2 <- union_merge %>% st_cast('POLYGON') %>% 
    as.data.frame() %>% st_as_sf()

  
   
  if (!exists("mega_join_clust_2")){
    mega_join_clust_2 <- remerge_v1v2
  }else {
    mega_join_clust_2 <- rbind(mega_join_clust_2,remerge_v1v2)
  }
  
  remove(union_xtract,union_x,union_xtract_x,union_xx,union_merge,remerge_v1v2,clst_adm_sel)
  print('End cycle 2')
  Sys.time() %>% print
}

#Get unique
mega_cent <- mega_join_clust_2 %>% st_centroid() %>% st_coordinates() %>%  as_data_frame()
mega_join_clust_2$sel_dup <- duplicated(mega_cent$X %>% round(2)) * duplicated(mega_cent$Y %>% round(2))
uniq_mrg_clt_xtract_cents <- mega_join_clust_2 %>% filter(sel_dup == 0)
uniq_mrg_clt_xtract_cents$sel_dup <- NULL

st_write(uniq_mrg_clt_xtract_cents,"r_results\\gh_join_clust_32630.shp")

Sys.time()














