###############################################################
## 
##  Sept 6th 
##  2050s. and observed. Special order Fabio. Linear models and params.
##

rm(list=ls())

library(dplyr)
library(data.table)
library(ggplot2)


source_path = "/home/hnoorazar/Sid/sidFabio/SidFabio_core_plot.R"
source_path = "/Users/hn/Documents/00_GitHub/Ag/Sids_Projects/Sid_Fabio/SidFabio_core_plot.R"
source(source_path)
options(digits=9)


################################
########
######## parameters
########
param_dir = "/Users/hn/Documents/01_research_data/Sid/SidFabio/parameters/"
veg_type = "tomato"  # "tomato" at this point, later: "carrot", "spinach", "strawberry", "tomato"

################################
########
######## Directories
########

data_dir_base = "/Users/hn/Documents/01_research_data/Sid/SidFabio/"
data_dir = paste0(data_dir_base, "/02_aggregate_Maturiry_EE_linear_Kamiak/", veg_type, "/special_order_Aug_30_email/")


out_dir = paste0(data_dir_base, "03_plots/specialOrder_2050s", veg_type, "/")
if (dir.exists(out_dir) == F) {
    dir.create(path = out_dir, recursive = T)
}

file_names = c("annual_means_within_CRD_properSpecialDoY.csv", 
               "within_TP_median_of_annual_means_within_CRD_properSpecialDoY.csv")
################################
########
########     read data
########

annual_means_within_CRD = data.table(read.csv(paste0(data_dir, file_names[1])))
within_TP_median_of_annual_means_within_CRD = data.table(read.csv(paste0(data_dir, file_names[2])))
fabio_future_close_startDoY = data.table(read.csv(paste0(param_dir, "fabio_future_close_startDoY.csv")))

chosen_CRD_alph <- c("CA40", "CA50", "CA51", "FL50", "MI80")

annual_means_within_CRD$CRD <- factor(annual_means_within_CRD$CRD, 
                                      levels = chosen_CRD_alph, order=TRUE)

within_TP_median_of_annual_means_within_CRD$CRD <- factor(within_TP_median_of_annual_means_within_CRD$CRD, 
                                                          levels = chosen_CRD_alph, order=TRUE)

start_DOY = sort(unique(annual_means_within_CRD$startDoY))
annual_means_within_CRD$startDoY <- factor(annual_means_within_CRD$startDoY, 
                                           levels = start_DOY, order=TRUE)
within_TP_median_of_annual_means_within_CRD$startDoY <- factor(within_TP_median_of_annual_means_within_CRD$startDoY, 
                                                               levels=start_DOY, order=TRUE)

################################
########
########    TS Plots
########
annual_TS_timePeriod_groupColor_specialOrder <- function(d1, colname="mean_days_to_maturity", fil="time_period"){
  ggplot(d1, aes(x=year, y=get(colname), colour=startDoY)) + # colour=fil
  geom_line(size=2) +
  facet_wrap(. ~ CRD)+  # ~ startDoY 
  labs(x="year", y = "average number of days to reach maturity", fill = fil) + #
  # guides(fill=guide_legend(title="Time period")) +
  # scale_color_manual(values=c("deepskyblue", "darkgreen", "orange")) +
  # scale_fill_manual(values=c("deepskyblue", "darkgreen", "orange")) +
  theme(panel.grid.major = element_line(size=0.2),
        panel.spacing=unit(.5, "cm"),
        legend.text=element_text(size=18, face="bold"),
        legend.title = element_blank(),
        # legend.position = "none",
        strip.text = element_text(face="bold", size=16, color="black"),
        axis.text = element_text(size=16, color="black"), # face="bold",
        # axis.text.x = element_text(angle=20, hjust = 1),
        axis.ticks = element_line(color = "black", size = .2),
        axis.title.x = element_text(size=18,  face="bold", 
                                    margin=margin(t=10, r=0, b=0, l=0)),
        axis.title.y = element_text(size=18, face="bold",
                                    margin=margin(t=0, r=10, b=0, l=0)),
        plot.title = element_text(lineheight=.8, face="bold", size=20)
        )
}

mean_days_to_maturity_plot<- annual_TS_timePeriod_groupColor_specialOrder(d1=annual_means_within_CRD, 
                                                                          colname="mean_days_to_maturity", 
                                                                          fil="time_period")

fName = paste("mean_days_to_maturity", veg_type, sep = "_")
ggsave(plot = mean_days_to_maturity_plot,
       filename = paste0(fName, ".png"), 
       width=15, height=7, units = "in", 
       dpi=200, device = "png",
       path=out_dir,
       limitsize = FALSE)



annual_TS_timePeriod_groupColor <- function(d1, colname="mean_days_to_maturity", fil="time_period"){
  ggplot(d1, aes(x=year, y=get(colname), colour=startDoY)) + # colour=fil
  geom_line(size=2) +
  facet_wrap(. ~ CRD)+
  labs(x="year", y = "average number of days to reach maturity", fill = fil) + #
  # guides(fill=guide_legend(title="Time period")) +
  scale_color_manual(values=c("deepskyblue", "darkgreen", "orange")) +
  scale_fill_manual(values=c("deepskyblue", "darkgreen", "orange")) +
  theme(panel.grid.major = element_line(size=0.2),
        panel.spacing=unit(.5, "cm"),
        legend.text=element_text(size=18, face="bold"),
        legend.title = element_blank(),
        legend.position = "bottom",
        strip.text = element_text(face="bold", size=16, color="black"),
        axis.text = element_text(size=16, color="black"), # face="bold",
        # axis.text.x = element_text(angle=20, hjust = 1),
        axis.ticks = element_line(color = "black", size = .2),
        axis.title.x = element_text(size=18,  face="bold", 
                                    margin=margin(t=10, r=0, b=0, l=0)),
        axis.title.y = element_text(size=18, face="bold",
                                    margin=margin(t=0, r=10, b=0, l=0)),
        plot.title = element_text(lineheight=.8, face="bold", size=20)
        )
}


for (a_crd in chosen_CRD_alph){
  annual_means_within_CRD_subset <- annual_means_within_CRD %>%
                                    filter(CRD==a_crd) %>%
                                    data.table()
 mean_days_to_maturity_plot<- annual_TS_timePeriod_groupColor(d1=annual_means_within_CRD_subset, 
                                        colname="mean_days_to_maturity", fil="maturity age")
 
 fName = paste("mean_days_to_maturity", veg_type, a_crd, sep = "_")

 subset_out_dir = paste0(out_dir, "mean_days_to_maturity_separate_CRD/")
  if (dir.exists(subset_out_dir) == F) {
      dir.create(path=subset_out_dir, recursive = T)
   }
 ggsave(plot = mean_days_to_maturity_plot,
        filename = paste0(fName, ".png"), 
        width=20, height=10, units = "in", 
        dpi=200, device = "png",
        path=subset_out_dir,
        limitsize = FALSE)
}


######## Useless
# for (a_start_DOY in start_DOY){
#   annual_means_within_CRD_subset <- annual_means_within_CRD %>%
#                                     filter(startDoY==a_start_DOY) %>%
#                                     data.table()

#   mean_days_to_maturity_plot<- annual_TS_timePeriod_groupColor(d1=annual_means_within_CRD_subset, 
#                                          colname="mean_days_to_maturity", fil="maturity age")
 
#   fName = paste("mean_days_to_maturity", veg_type, a_start_DOY, sep = "_")

#   subset_out_dir = paste0(out_dir, "mean_days_to_maturity_separate_start_DoY/")
#    if (dir.exists(subset_out_dir) == F) {
#        dir.create(path=subset_out_dir, recursive = T)
#     }
#   ggsave(plot = mean_days_to_maturity_plot,
#          filename = paste0(fName, ".png"), 
#          width=20, height=7.5, units = "in",
#          dpi=200, device = "png",
#          path=subset_out_dir,
#          limitsize = FALSE)
# }

################################
########
########    Box Plots
########

box_annual_means_within_CRD=box_annual_startDoY_x(dt=annual_means_within_CRD, 
                                                  colname="mean_days_to_maturity", 
                                                  title_="Fabio Aug 30 email: tomato, linear model and linear params.",
                                                  yLab="average number of days to maturity"
                                                  )

# param_type="fabio"
fName = paste("box_mean_days_to_maturity", veg_type, sep = "_")
ggsave(plot = box_annual_means_within_CRD,
       filename = paste0(fName, ".png"), 
       width=17, height=4, units = "in", 
       dpi=200, device = "png",
       path=out_dir,
       limitsize = FALSE)



