####
#### This module generates #s in the following link ()
#### https://docs.google.com/document/d/18KX24FkL70_Xhxagwx9EBRWeQmz-Ud-iuTXqnf9YXnk/edit?usp=sharing
####

rm(list=ls())
library(data.table)
library(rgdal)
library(dplyr)
library(sp)
# library(sf)
library(foreign)

source_1 = "/Users/hn/Documents/00_GitHub/Ag/remote_sensing/R/remote_core.R"
source(source_1)
options(digits=9)
options(digit=9)

##############################################################################

data_dir <- paste0("/Users/hn/Documents/01_research_data/remote_sensing/00_shapeFiles/0002_final_shapeFiles/000_Eastern_WA/")

##############################################################################

WSDA <- readOGR(paste0(data_dir, "Eastern_", SF_year, "/Eastern_", 2017, ".shp"),
                       layer = paste0("Eastern_", SF_year), 
                       GDAL1_integer64_policy = TRUE)


Grant <- WSDA[grepl('Grant', WSDA$county), ]


write_dir <- paste0("/Users/hn/Documents/01_research_data/remote_sensing/00_shapeFiles/0002_final_shapeFiles/")
writeOGR(obj = Grant, 
         dsn = paste0(write_dir, "/", "Grant2017"), 
         layer = "Grant2017", 
         driver = "ESRI Shapefile")


WSDA <- readOGR(paste0(data_dir, "Eastern_", SF_year, "/Eastern_", 2016, ".shp"),
                       layer = paste0("Eastern_", SF_year), 
                       GDAL1_integer64_policy = TRUE)


Adam <- WSDA[grepl('Adam', WSDA$county), ]
Benton <- WSDA[grepl('Benton', WSDA$county), ]
Adam <- raster::bind(Adam, Benton)

write_dir <- paste0("/Users/hn/Documents/01_research_data/remote_sensing/00_shapeFiles/0002_final_shapeFiles/")
writeOGR(obj = Adam, 
         dsn = paste0(write_dir, "/", "AdamBenton2016"), 
         layer = "AdamBenton2016", 
         driver = "ESRI Shapefile")


WSDA <- readOGR(paste0(data_dir, "Eastern_", SF_year, "/Eastern_", 2016, ".shp"),
                       layer = paste0("Eastern_", SF_year), 
                       GDAL1_integer64_policy = TRUE)


Franklin <- WSDA[grepl('Franklin', WSDA$county), ]
Yakima <- WSDA[grepl('Yakima', WSDA$county), ]
Franklin <- raster::bind(Franklin, Yakima)

write_dir <- paste0("/Users/hn/Documents/01_research_data/remote_sensing/00_shapeFiles/0002_final_shapeFiles/")
writeOGR(obj = Franklin, 
         dsn = paste0(write_dir, "/", "FranklinYakima2018"), 
         layer = "FranklinYakima2018", 
         driver = "ESRI Shapefile")

