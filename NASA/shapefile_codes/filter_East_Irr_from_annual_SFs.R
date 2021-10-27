################################################################################
#####
#####    Oct. 26, 2021
#####
#####    Goal: Clean up the damn WSDA shapefiles so, Supria can intersect it.
#####          Pick up East, Irrigated fields, and, keep only common useful columns.
#####          
#####
##### 
#####

rm(list=ls())
library(data.table)
library(rgdal)
library(dplyr)
library(sp)
library(sf)
library(foreign)

source_1 = "/Users/hn/Documents/00_GitHub/Ag/remote_sensing/R/remote_core.R"
source(source_1)
options(digits=9)
options(digit=9)


##############################################################################################################
#
#    Directory setup
#
SF_dir <- paste0("/Users/hn/Documents/01_research_data/NASA/shapefiles/WSDA_separateYears/")
output_dir <- paste0("/Users/hn/Documents/01_research_data/NASA/shapefiles/")
if (dir.exists(output_dir) == F) {dir.create(path = output_dir, recursive = T)}

##############################################################################################################
#
#    Body
#

start_time <- Sys.time()

years <- c(2008:2020)

for (yr in years){
  SF <- readOGR(paste0(SF_dir, "WSDA_EW_", yr, ".shp"),
                layer = paste0("WSDA_EW_", yr), 
                GDAL1_integer64_policy = TRUE)

  SF@data <- within(SF@data, remove(Acres, CropGroup, CoverCrop, InitialSur, NLCD_Cat,
                                    Notes, Organic, RotCropGro, Rot1CropGr, Rot1Crop, 
                                    RotationCr, RotCropTyp, Rot1CropTy, Rot2CropGr, 
                                    Rot2CropTy, Shape_Area, Shape_Leng, SHAPE_Area, 
                                    SHAPE_Leng, TotalAcres, TRS))

  if ("Source" %in% colnames(SF@data)){
    setnames(SF@data, old=c("Source"), new=c("DataSource"))
  }

  if ("DataSrc" %in% colnames(SF@data)){
    setnames(SF@data, old=c("DataSrc"), new=c("DataSource"))
  }
  
  if ("Exact_Acre" %in% colnames(SF@data)){
    setnames(SF@data, old=c("Exact_Acre"), new=c("ExactAcres"))
  }

  setnames(SF@data, 
           old=c("CropType", "DataSource", "LastSurvey", "OBJECTID", "Irrigation", "ExactAcres"), 
           new=c("CropTyp",  "DataSrc",    "LstSrvD",    "ID",       "Irrigtn",    "ExctAcr"))

  SF@data$ID <- as.character(SF@data$ID)
  SF@data$ID <- paste0(yr, "_", SF@data$ID)

  # cols <- c("ExctAcr")
  # SF@data <- data.table(SF@data)
  # SF@data[,(cols) := round(.SD, 2), .SDcols=cols]

  SF@data$Irrigtn <- tolower(SF@data$Irrigtn)
  SF@data$CropTyp <- tolower(SF@data$CropTyp)
  SF@data$DataSrc <- tolower(SF@data$DataSrc)

  SF <- pick_eastern_counties(SF)

  writeOGR(obj = SF, 
           dsn = paste0(output_dir, "/WSDA_separateYears_East_cleanCols/", "/WSDA_EW_", yr, "_cleanCols/"), 
           layer = paste0("WSDA_EW_", yr, "_cleanCols"), 
           driver="ESRI Shapefile")

  
  print (sort(colnames(colnames)))
  ############################################################
  #
  # pick up fucking irrigated fields
  #
  ############################################################
  SF@data$Irrigtn <- tolower(SF@data$Irrigtn)
  SF@data$Irrigtn[is.na(SF@data$Irrigtn)] <- "na"

  SF <- SF[!grepl('none', SF$Irrigtn), ]    # toss out those with None in irrigation
  SF <- SF[!grepl('unknown', SF$Irrigtn), ] # toss out Unknown
  SF <- SF[!grepl('na', SF$Irrigtn), ]      # toss out NAs
  
  writeOGR(obj = SF, 
           dsn = paste0(output_dir, "/WSDA_separateYears_East_Irr_cleanCols/", "/WSDA_EW_Irr_", yr, "_cleanCols"), 
           layer = paste0("/WSDA_EW_Irr_", yr, "_cleanCols"), 
           driver="ESRI Shapefile")
}


