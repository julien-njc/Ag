#######################################################
#####
#####    Oct. 25, 2021
#####
#####    Goal: compute how much of the fields are have None or Unknow or None/X
#####          
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

col_names <- c("SF_year", "total_acr", "None_acr", "None_combo_acr", "unknown_acr", "NA_acr")
damn_output <- setNames(data.table(matrix(nrow = length(years), 
                                          ncol = length(col_names))), 
                        col_names)
damn_output$SF_year <- years

damn_output$SF_year <- as.numeric(damn_output$SF_year)
damn_output$total_acr <- as.numeric(damn_output$total_acr)
damn_output$None_acr <- as.numeric(damn_output$None_acr)
damn_output$None_combo_acr <- as.numeric(damn_output$None_combo_acr)
damn_output$unknown_acr <- as.numeric(damn_output$unknown_acr)
damn_output$NA_acr <- as.numeric(damn_output$NA_acr)


correct_year_out <- copy(damn_output)

for (yr in years){
  SF <- readOGR(paste0(SF_dir, "WSDA_EW_", yr, ".shp"),
                layer = paste0("WSDA_EW_", yr), 
                GDAL1_integer64_policy = TRUE)

  SF <- SF@data
  SF <- within(SF, remove(Notes))

  colnames(SF)[colnames(SF)=="County"] <- "county"

  SF <- pick_eastern_counties(SF)
  colnames(SF)[colnames(SF)=="ExactAcres"] <- "Exact_Acre"
  print (sort(colnames(colnames)))

  SF$Irrigation[is.na(SF$Irrigation)] <- "na"

  SF$Irrigation <- tolower(SF$Irrigation)

  damn_output[SF_year == yr, "total_acr"] <- sum(SF$Exact_Acre)
  
  unknown <- SF %>% filter(Irrigation == "unknown") %>% data.table()
  damn_output[SF_year == yr, "unknown_acr"] <- sum(unknown$Exact_Acre)

  na <- SF %>% filter(Irrigation == "na") %>% data.table()
  damn_output[SF_year == yr, "NA_acr"] <- sum(na$Exact_Acre)


  none_and_NoneCombo <- SF[grepl('none', SF$Irrigation), ]
  none <- SF %>% filter(Irrigation == "none") %>% data.table()

  damn_output[SF_year == yr, "None_acr"] <- sum(none$Exact_Acre)
  damn_output[SF_year == yr, "None_combo_acr"] <- (sum(none_and_NoneCombo$Exact_Acre) - sum(none$Exact_Acre))


  #### repeat the damn thing for correct survey year
  SF_correctYear <- SF[grepl(as.character(yr), SF$LastSurvey), ]

  correct_year_out[SF_year == yr, "total_acr"] <- sum(SF_correctYear$Exact_Acre)

  unknown <- SF_correctYear %>% filter(Irrigation == "unknown") %>% data.table()
  correct_year_out[SF_year == yr, "unknown_acr"] <- sum(unknown$Exact_Acre)

  na <- SF_correctYear %>% filter(Irrigation == "na") %>% data.table()
  correct_year_out[SF_year == yr, "NA_acr"] <- sum(na$Exact_Acre)


  none_and_NoneCombo <- SF_correctYear[grepl('none', SF_correctYear$Irrigation), ]
  none <- SF_correctYear %>% filter(Irrigation == "none") %>% data.table()

  correct_year_out[SF_year == yr, "None_acr"] <- sum(none$Exact_Acre)
  correct_year_out[SF_year == yr, "None_combo_acr"] <- (sum(none_and_NoneCombo$Exact_Acre) - sum(none$Exact_Acre))
}

damn_output$non_irrigated <- damn_output$total_acr + damn_output$None_acr + damn_output$None_combo_acr + 
                            damn_output$unknown_acr + damn_output$NA_acr 

correct_year_out$non_irrigated <- correct_year_out$total_acr + correct_year_out$None_acr + 
                                 correct_year_out$None_combo_acr + correct_year_out$unknown_acr + 
                                 correct_year_out$NA_acr 



cols <- names(correct_year_out)[2:7]
correct_year_out[,(cols) := round(.SD,1), .SDcols=cols]
damn_output[,(cols) := round(.SD,1), .SDcols=cols]

write.csv(correct_year_out, paste0(output_dir, "nonIrrigatedArea_correctYear.csv"), row.names = F)
write.csv(damn_output, paste0(output_dir, "nonIrrigatedArea.csv"), row.names = F)



