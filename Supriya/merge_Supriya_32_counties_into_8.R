rm(list=ls())
library(data.table)
library(rgdal)
library(sp)
library(dplyr)
library(ggplot2)
library(maps)
library(purrr)
library(scales) # includes pretty_breaks

##############################################################################################################
#
#    Directory setup
#

base_dir <- "/Users/hn/Documents/01_research_data/Supriya/Shapefiles_landsatcode_NDVIAnalysis/32_counties_ino_6/1km_CountyGrid/"
sub_dirs <- c("CA", "CO", "FL", "ME", "MI", "NY", "TX", "WA")
output_dir <- base_dir


for (sub in sub_dirs){
  print ("__________________________________________________________________")
  print (sub)
  
  SF_dir <- paste0(base_dir, sub, "/")
  shapeFile_list <- list.files(path = paste0(base_dir, sub, "/"), pattern = ".shp")

  ########################################

  if (length(shapeFile_list) > 1){
    all_1KM_grids <- readOGR(paste0(SF_dir, shapeFile_list[1]),
                          layer = stringr::str_replace(shapeFile_list[1], ".shp", replacement=""), 
                          GDAL1_integer64_policy = TRUE)
    counter = 2
    for (a_damn_SF in shapeFile_list[c(2:length(shapeFile_list))]){

      fucking_SF <- readOGR(paste0(SF_dir, a_damn_SF),
                            layer = stringr::str_replace(a_damn_SF, ".shp", replacement=""), 
                            GDAL1_integer64_policy = TRUE);

      if ("grid_is" %in% colnames(fucking_SF@data)){
        setnames(fucking_SF@data, old=c("grid_is"), new=c("grid_id"))
      }
      
      fucking_SF@data$grid_id <- fucking_SF@data$grid_id + max(all_1KM_grids@data$grid_id)
      
      all_1KM_grids <- rbind(all_1KM_grids, fucking_SF)

      print (a_damn_SF)
      print (counter)
      counter = counter+1
    }


    all_1KM_grids@data <- within(all_1KM_grids@data, remove("id"))


    writeOGR(obj = all_1KM_grids, 
             dsn = paste0(base_dir, "/all_", sub), 
             layer= paste0("/all_", sub), 
             driver="ESRI Shapefile")

  } else {
    all_1KM_grids <- readOGR(paste0(SF_dir, shapeFile_list[1]),
                          layer = stringr::str_replace(shapeFile_list[1], ".shp", replacement=""), 
                          GDAL1_integer64_policy = TRUE)
    if ("grid_is" %in% colnames(fucking_SF@data)){
        setnames(fucking_SF@data, old=c("grid_is"), new=c("grid_id"))
      }
      fucking_SF@data$grid_id <- fucking_SF@data$grid_id + max(all_1KM_grids@data$grid_id)

    all_1KM_grids@data <- within(all_1KM_grids@data, remove("id"))

    writeOGR(obj = all_1KM_grids, 
             dsn = paste0(base_dir, "/all_", sub), 
             layer= paste0("/all_", sub), 
             driver="ESRI Shapefile")
  }
}
