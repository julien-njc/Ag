.libPaths("/data/hydro/R_libs35")
.libPaths()
library(data.table)
source_path = "/home/hnoorazar/sid/sidFabio/SidFabio_core.R"
source(source_path)
options(digit=9)
options(digits=9)

######################################################################
##                                                                  ##
##              Terminal/shell/bash arguments                       ##
##                                                                  ##
######################################################################

args = commandArgs(trailingOnly=TRUE)
veg_type = args[1]
model_type = args[2]
start_doy = args[3]

######################################################################
# Define main output path
out_dir = "/data/hydro/users/Hossein/Sids_Projects/SidFabio/"

# 2a. Only use files in geographic locations we're interested in
param_dir = file.path("/data/hydro/users/Hossein/Sids_Projects/SidFabio/000_parameters/")

if (veg_type=="tomato"){
  file_list = "VIC_tomato_points.txt"
}

local_files <- read.delim(file = paste0(param_dir, file_list), 
                          header=FALSE, as.is=TRUE)
local_files <- as.vector(local_files$V1)

veg_params <- data.table(read.csv(paste0(param_dir, "veg_params.csv"),  as.is=T))
veg_params=veg_params[veg_params$veg==veg_type]

maturity_cumGDD=veg_params$maturity_gdd

# 3. Process the data -----------------------------------------------------
# Time the processing of this batch of files
start_time <- Sys.time()


dir_base <- "/data/hydro/users/Hossein/Sids_Projects/SidFabio/00_cumGDD/"
data_dir <- paste0(dir_base, veg_type, "/", model_type, "/")

col_names <- c("location", "year", "days_to_maturity")

# 36 below comes from 1980-2015.
if (model_type=="observed"){
  days_to_maturity <- setNames(data.table(matrix(nrow = length(local_files)*36, 
                                                 ncol = length(col_names))), col_names)

  days_to_maturity$location <- rep.int(local_files, 36)
  setorderv(days_to_maturity,  ("location"))
  days_to_maturity$year <- rep.int(c(1980:2015), length(local_files))
}


# x <- sapply(local_files, 
#             function(x) strsplit(x, "_")[[1]], 
#             USE.NAMES=FALSE)
# lat = x[2, ]
# long = x[3, ]

for(fileName in local_files){
  # The following function will look into the right directory when 
  data <- data.table(read.csv(paste0(data_dir, fileName, ".csv")))
  data$row_num <- seq.int(nrow(data))

  # data <- data %>%
  #         select(-c(precip, windspeed, SPH, SRAD, Rmax, Rmin))

  # data[, cum_GDD:=NULL] # cum_GDD is useless. I need to do this on yearly basis.

  for (a_year in sort(unique(days_to_maturity$year))){
    curr_row_num <- data[data$year==a_year & doy==start_doy]$row_num
    curr_data <- data[data$row_num>=curr_row_num]
    curr_data$cumGDD <- 0
    curr_data[, cum_GDD := cumsum(daily_GDD)] # , by=list(year)

    day_of_maturity=curr_data[curr_data$cum_GDD >= maturity_cumGDD]
    dayCount = day_of_maturity$row_num[1]-curr_data$row_num[1]
    days_to_maturity$days_to_maturity[days_to_maturity$location==fileName & days_to_maturity$year==a_year] = dayCount

  }  
}

current_out = paste0(out_dir, "/days_to_maturity/", veg_type, "/") # "_", model_type, 
if (dir.exists(current_out) == F) {
    dir.create(path = current_out, recursive = T)
}

write.csv(days_to_maturity, 
          file = paste0(current_out, model_type, "_days_to_maturity.csv"), 
          row.names=FALSE)



# How long did it take?
end_time <- Sys.time()
print( end_time - start_time)
