
for(h in unique(stats_comp$model)) {
  assign(x = paste(gsub(pattern = "-", replacement = "_", x = h), "map", "jan45", sep="_"),
         value ={ model_map(model = h, scenario_name = "rcp45", month_col = "median_J1",
                     min = accum_jan45_min, max = accum_jan45_max)
                }
       )
}


# Need to add historical observed to this:
accum_jan45_figs <- ggarrange(plotlist = list(observed_map_jan45,
                                              ensemble_map_jan45,
                                              bcc_csm1_1_m_map_jan45,
                                              bcc_csm1_1_map_jan45,
                                              BNU_ESM_map_jan45,
                                              CanESM2_map_jan45,
                                              CCSM4_map_jan45, 
                                              CNRM_CM5_map_jan45,
                                              CSIRO_Mk3_6_0_map_jan45,
                                              GFDL_ESM2G_map_jan45,
                                              GFDL_ESM2M_map_jan45,
                                              HadGEM2_CC365_map_jan45,
                                              HadGEM2_ES365_map_jan45,
                                              inmcm4_map_jan45,
                                              IPSL_CM5A_LR_map_jan45, 
                                              IPSL_CM5A_MR_map_jan45,
                                              IPSL_CM5B_LR_map_jan45,
                                              MIROC_ESM_CHEM_map_jan45,
                                              MIROC5_map_jan45, 
                                              MRI_CGCM3_map_jan45,
                                              NorESM1_M_map_jan45),
                              ncol = 2, nrow = 11,
                              common.legend = TRUE)