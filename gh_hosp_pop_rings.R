

library(sf)
library(raster)
require(exactextractr)

setwd("C:\\rli\\ghana_project")
datapath<-("C:\\rli\\ghana_project")

gh_hosp <- st_read(file.path(datapath,"source_data\\02_Healthsites\\gh_health_facilities_32630.shp"))%>% 
  st_transform(32630) %>% filter(!is.na(Latitude)) 
hrsl_population_rast <- raster(file.path(datapath,"source_data\\02_population\\stretched\\population_gha_2018-10-01.tif"))
gh_adm_0 <- st_read(file.path(datapath,"source_data\\01_Administrative_Boundaries\\GHA_admbndp0_1m_GAUL.shp"))


gh_pop <- exact_extract(hrsl_population_rast, gh_adm_0,'sum')
gh_adm_0$total_pop <- gh_pop



#d_rings <- seq(5000,35000, by=5000) 
d_rings <- seq(500,5000, by=500) 

#d_rings <- d_rings[1]
c_numb <- length(gh_adm_0) +1


for (i in d_rings){
  print(i)
  hos_buff <- st_buffer(gh_hosp,i) %>% st_union() %>% st_transform(4326)%>% st_intersection(gh_adm_0) 
  sum_pop <- exact_extract(hrsl_population_rast, hos_buff,'sum')
  
  gh_adm_0$new_c <- sum_pop
  col_name <- paste("buff_",i, sep = "")
  colnames(gh_adm_0)[c_numb]=col_name
  c_numb <- c_numb + 1
  
}


colnames(gh_adm_0)[24] <- "buff_5000_2" 

st_write(gh_adm_0,"source_data\\02_Healthsites\\r_test_results\\gh_health_facilities_pop_rings_coverage_v4.shp")




hos_buff <- st_buffer(gh_hosp,35000)  %>% st_union() %>% st_transform(4326) %>% st_intersection(gh_adm_0) 
plot(hos_buff)
st_write(hos_buff,"source_data\\02_Healthsites\\r_test_results\\gh_health_facilities_pop_rings_buff_35000_clipped.shp")

sum_pop <- exact_extract(hrsl_population_rast, hos_buff,'sum')

























