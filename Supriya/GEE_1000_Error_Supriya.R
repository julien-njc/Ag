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

SF_dir <- paste0("/Users/hn/Downloads/GEE_Error_when_features_have_more_than_1000000_vertices/")

GEE_1000_error <- readOGR(paste0(SF_dir, "AZ_2020.shp"),
                          layer = "AZ_2020", 
                          GDAL1_integer64_policy = TRUE)

writeOGR(obj = GEE_1000_error, 
         dsn = paste0(SF_dir, "/AZ_2020_R/"), 
         layer="AZ_2020_R", 
         driver="ESRI Shapefile")


# If you want to simplify:
GEE_1000_error_simple <- rmapshaper::ms_simplify(GEE_1000_error)



states <- map_data("state")
states_cluster <- subset(states, region %in% c("arizona"))

Error_map <- ggplot() +
             geom_polygon(data = states_cluster, aes(x=long, y=lat, group=group), fill = "grey", color = "black") +
             geom_polygon(data = GEE_1000_error, aes(x=long, y=lat, group=group), fill = "grey47", color = "red") + 
             coord_sf(xlim = c(-1500000, -1000000), ylim = c(1100000, 1500000)) # <----- see if this works

plot_w <- 5
plot_h <- 5
ggsave(filename = paste0("Error_map.pdf"),
       plot = Error_map, 
       width = plot_w, height = plot_h, units = "in", limitsize = FALSE,
       dpi = 400, device = "pdf",
       path = SF_dir)


# If you want to simplify:
GEE_1000_error_simple <- rmapshaper::ms_simplify(GEE_1000_error)

Error_map_simple <- ggplot() +
                    geom_polygon(data = states_cluster, aes(x=long, y=lat, group=group), fill = "grey", color = "black") +
                    geom_polygon(data = GEE_1000_error_simple, aes(x=long, y=lat, group=group), fill = "grey47", color = "red") + 
                    coord_sf(xlim = c(-1500000, -1000000), ylim = c(1100000, 1500000)) # <----- see if this works

ggsave(filename = paste0("Error_map_simple.pdf"),
       plot = Error_map_simple, 
       width = plot_w, height = plot_h, units = "in", limitsize = FALSE,
       dpi = 400, device = "pdf",
       path = SF_dir)




###################################
###################################   CRS change
###################################
crs <- CRS("+proj=lcc 
           +lat_1=45.83333333333334 
           +lat_2=47.33333333333334 
           +lat_0=45.33333333333334 
           +lon_0=-120.5 +datum=WGS84")

GEE_1000_error_CRS <- spTransform(GEE_1000_error, 
                                  CRS("+proj=longlat +datum=WGS84"))


Error_map_CRS <- ggplot() +
                 geom_polygon(data = states_cluster, aes(x=long, y=lat, group=group), fill = "grey", color = "black") +
                 geom_polygon(data = GEE_1000_error_CRS, aes(x=long, y=lat, group=group), fill = "grey47", color = "red")

plot_w <- 5
plot_h <- 5
ggsave(filename = paste0("Error_map_CRS.pdf"),
       plot = Error_map_CRS, 
       width = plot_w, height = plot_h, units = "in", limitsize = FALSE,
       dpi = 400, device = "pdf",
       path = SF_dir)

###################################
###################################
###################################
#
# If you want to simplify:
#
GEE_1000_error_CRS_simple <- rmapshaper::ms_simplify(GEE_1000_error_CRS)

writeOGR(obj = GEE_1000_error_CRS_simple, 
         dsn = paste0(SF_dir, "/AZ_2020_R_GEE_1000_error_CRS_simple/"), 
         layer="AZ_2020_R", 
         driver="ESRI Shapefile")


Error_map_CRS_simple <- ggplot() +
                        geom_polygon(data = states_cluster, aes(x=long, y=lat, group=group), fill = "grey", color = "black") +
                        geom_polygon(data = GEE_1000_error_CRS_simple, aes(x=long, y=lat, group=group), fill = "grey47", color = "red")

ggsave(filename = paste0("Error_map_CRS_simple.pdf"),
       plot = Error_map_CRS_simple, 
       width = plot_w, height = plot_h, units = "in", limitsize = FALSE,
       dpi = 400, device = "pdf",
       path = SF_dir)


