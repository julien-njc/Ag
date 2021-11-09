import matplotlib.pyplot as plt
import seaborn as sb
import sys
import scipy
import scipy.signal
import matplotlib.dates as mdates
sys.path.append('/Users/hn/Documents/00_GitHub/Ag/NASA/Python_codes/')
sys.path.append('/home/hnoorazar/NASA/')
import NASA_core as nc


def SG_clean_SOS(raw_dt, SG_dt, idx, ax, onset_cut=0.5, offset_cut=0.5):
    """Returns A plot with of a given VI (NDVI or EVI) with SOS and EOS points.

    Arguments
    ---------
    raw_dt : dataframe
        pandas dataframe of raw observations from Google Earth Engine
    
    SG_dt  : dataframe
        pandas dataframe of smoothed version of data points.
    
    idx : str
        A string indicating vegetation index.
    
    ax : axis
       An axis object of Matplotlib.
    
    onset_cut : float
        Start Of Season threshold
    offset_cut : float
        End Of Season threshold

    Returns
    -------
    A plot a given VI (NDVI or EVI) with SOS and EOS points.
    """
    assert (len(SG_dt['ID'].unique()) == 1)

    #############################################
    ###
    ###      find SOS's and EOS's
    ###
    #############################################
    SEOS_output_columns = ['ID', indeks, 'human_system_start_time', 
                           'EVI_ratio', 'SOS', 'EOS', 'season_count']

    """
     The reason I am multiplying len(a_df) by 4 is that we can have at least two
     seasons which means 2 SOS and 2 EOS. So, at least 4 rows are needed.
     and the reason for 14 is that there are 14 years from 2008 to 2021.
    """
    all_poly_and_SEOS = pd.DataFrame(data = None, 
                                     index = np.arange(4*14*len(a_df)), 
                                     columns = SEOS_output_columns)
    unique_years = SG_dt['human_system_start_time'].dt.year.unique()
    
    pointer_SEOS_tab = 0
    SG_dt = SG_dt[SEOS_output_columns[0:3]]
    
    """
    detect SOS and EOS in each year
    """
    yr_count = 0
    for yr in unique_years:
        curr_field_yr = SG_dt[SG_dt['human_system_start_time'].dt.year == yr].copy()

        curr_field_yr = nc.addToDF_SOS_EOS_White(pd_TS = curr_field_yr, 
                                                 VegIdx = indeks, 
                                                 onset_thresh = onset_cut, 
                                                 offset_thresh = offset_cut)
        curr_field_yr = nc.Null_SOS_EOS_by_DoYDiff(pd_TS=curr_field_yr, min_season_length=40)
            
        #############################################
        ###
        ###             plot
        ###
        #############################################
        # sb.set();
        # plot SG smoothed
        # ax.plot(SG_dt['human_system_start_time'], SG_dt[idx], label= "SG", c='k', linewidth=2);
        ax.plot(SG_dt['human_system_start_time'], SG_dt[idx], c='k', linewidth=2,
                label= 'SG' if yr_count == 0 else "");


        # plot raw data
        ax.scatter(raw_dt['human_system_start_time'], 
                   raw_dt[idx], 
                   s=7, c='dodgerblue', label="raw" if yr_count == 0 else "");


        ###
        ###   plot SOS and EOS
        ###
        # Update the EVI/NDVI values to the smoothed version.
        #
        #  Start of the season
        #
        SOS = curr_field_yr[curr_field_yr['SOS'] != 0]
        ax.scatter(SOS['human_system_start_time'], SOS['SOS'], marker='+', s=155, c='g')
        # annotate SOS
        for ii in np.arange(0, len(SOS)):
            style = dict(size=10, color='g', rotation='vertical')
            ax.text(x = SOS.iloc[ii]['human_system_start_time'].date(), 
                    y = -0.2, 
                    s = str(SOS.iloc[ii]['human_system_start_time'].date())[6:], #
                    **style)

        #
        #  End of the season
        #
        EOS = curr_field_yr[curr_field_yr['EOS'] != 0]
        ax.scatter(EOS['human_system_start_time'], EOS['EOS'], marker='+', s=155, c='r')

        # annotate EOS
        for ii in np.arange(0, len(EOS)):
            style = dict(size=10, color='r', rotation='vertical')
            ax.text(x = EOS.iloc[ii]['human_system_start_time'].date(), 
                    y = -0.2, 
                    s = str(EOS.iloc[ii]['human_system_start_time'].date())[6:], #[6:]
                    **style)

        # Plot ratios:
        column_ratio = idx + "_" + "ratio"
        ax.plot(curr_field_yr['human_system_start_time'], 
                curr_field_yr[column_ratio], 
                c='gray', label="EVI Ratio" if yr_count == 0 else "")
        yr_count += 1

    ax.axhline(0 , color = 'r', linewidth=.5)
    ax.axhline(1 , color = 'r', linewidth=.5)

    ax.set_title(SG_dt['ID'].unique()[0]);
    ax.set(ylabel=idx)
    ax.set_xlim([datetime.date(2007, 12, 10), datetime.date(2022, 1, 10)])
    ax.set_ylim([-0.3, 1.15])
    ax.xaxis.set_major_locator(mdates.YearLocator(1)) # every year.
    ax.legend(loc="upper left");
#    legend_without_duplicate_labels(ax)

def legend_without_duplicate_labels(ax):
    ax.legend(loc="upper left");
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique))


def one_satellite_smoothed(raw_dt, ax, color_dict, idx="NDVI", time_step_size=10, set_negatives_to_zero=True):
    """Returns a dataframe that has replaced the missing parts of regular_TS.

    Arguments
    ---------
    raw_dt : dataframe
        A datafram of raw values from GEE. i.e. not regularized yet. F
        For a given field and a given satelltite

    ax : axis
        An axis object of Matplotlib.

    idx : string
        A string indicating vegetation index.

    time_step_size : integer
        An integer that is the regularization window size: every 10 days we want a given NDVI.

    Returns
    -------
    """
    a_df = raw_dt.copy()
    a_df.loc[a_df[idx]<0, idx] = 0

    assert (len(a_df.ID.unique()) == 1)
    assert (len(a_df.dataset.unique()) == 1)

    a_regularized_TS = nc.regularize_a_field(a_df, V_idks = idx, interval_size = time_step_size)
    # a_regularized_TS_noGap = nc.fill_theGap_linearLine(a_regularized_TS.copy(), V_idx=idx)
    a_regularized_TS_noGap = nc.fill_theGap_linearLine(a_regularized_TS, V_idx=idx)

    # Smoothen by Savitzky-Golay
    SG = scipy.signal.savgol_filter(a_regularized_TS_noGap[idx].values, window_length=7, polyorder=3)

    # SG might violate the boundaries. clip them:
    SG[SG > 1 ] = 1
    SG[SG < -1 ] = -1

    ax.plot(a_regularized_TS_noGap['human_system_start_time'], SG,
            '-', label="SG", 
            linewidth=1.25, color=color_dict[a_df.dataset.unique()[0]]) # , alpha=0.8

    ax.set_title(a_df.ID.unique()[0] + ", " + a_df.CropTyp.unique()[0])
    ax.set_ylabel(idx) # , labelpad=20); # fontsize = label_FontSize,
    ax.tick_params(axis='y', which='major') #, labelsize = tick_FontSize)
    ax.tick_params(axis='x', which='major') #, labelsize = tick_FontSize) # 
    # ax.legend(loc="lower right");
    # ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.set_ylim(-0.5, 1)


def all_satellite_smoothed(raw_dt, ax, color_dict, idx="NDVI", time_step_size=10, set_negatives_to_zero=True):
    """Returns a dataframe that has replaced the missing parts of regular_TS.

    Arguments
    ---------
    raw_dt : dataframe
        A datafram of raw values from GEE. i.e. not regularized yet. F
        For a given field and a given satelltite

    ax : axis
        An axis object of Matplotlib.

    idx : string
        A string indicating vegetation index.

    time_step_size : integer
        An integer that is the regularization window size: every 10 days we want a given NDVI.

    Returns
    -------
    """
    a_df = raw_dt.copy()
    a_df.loc[a_df[idx]<0 , idx] = 0

    assert (len(a_df.ID.unique()) == 1)
    assert (len(a_df.dataset.unique()) == 1)

    if a_df.dataset.unique()== "Landsat7_8day_NDVIComposite":
        # Smoothen by Savitzky-Golay
        SG = scipy.signal.savgol_filter(a_df[idx].values, window_length=7, polyorder=2)

        # SG might violate the boundaries. clip them:
        SG[SG > 1 ] = 1
        SG[SG < -1 ] = -1

        ax.plot(a_df['human_system_start_time'], SG,
                '-', label=(a_df.dataset.unique()[0] + " SG"), 
                linewidth=1.25, color=color_dict[a_df.dataset.unique()[0]])

        ax.set_title(a_df.ID.unique()[0] + ", " + a_df.CropTyp.unique()[0])
        ax.set_ylabel(idx) # , labelpad=20); # fontsize = label_FontSize,
        ax.tick_params(axis='y', which='major') #, labelsize = tick_FontSize)
        ax.tick_params(axis='x', which='major') #, labelsize = tick_FontSize) # 
        # ax.legend(loc="lower right");
        ax.xaxis.set_major_locator(mdates.YearLocator(1))
        ax.set_ylim(a_df[idx].min()-0.05, 1)
    else:
        a_regularized_TS = nc.regularize_a_field(a_df, V_idks = idx, interval_size = time_step_size)
        # a_regularized_TS_noGap = nc.fill_theGap_linearLine(a_regularized_TS.copy(), V_idx=idx)
        a_regularized_TS_noGap = nc.fill_theGap_linearLine(a_regularized_TS, V_idx=idx)

        # Smoothen by Savitzky-Golay
        SG = scipy.signal.savgol_filter(a_regularized_TS_noGap[idx].values, window_length=7, polyorder=3)

        # SG might violate the boundaries. clip them:
        SG[SG > 1 ] = 1
        SG[SG < -1 ] = -1

        ax.plot(a_regularized_TS_noGap['human_system_start_time'], SG,
                '-', label=(a_df.dataset.unique()[0] + " SG"), 
                linewidth=1.25, color=color_dict[a_df.dataset.unique()[0]]) # , alpha=0.8

        ax.set_title(a_df.ID.unique()[0] + ", " + a_df.CropTyp.unique()[0])
        ax.set_ylabel(idx) # , labelpad=20); # fontsize = label_FontSize,
        ax.tick_params(axis='y', which='major') #, labelsize = tick_FontSize)
        ax.tick_params(axis='x', which='major') #, labelsize = tick_FontSize) # 
        # ax.legend(loc="lower right");
        ax.xaxis.set_major_locator(mdates.YearLocator(1))
        ax.set_ylim(-0.5, 1)




def plot_8dayComposite_and_SG(raw_dt, ax, idx="NDVI"):
    a_df = raw_dt.copy()

    # Smoothen by Savitzky-Golay
    SG = scipy.signal.savgol_filter(a_df[idx].values, window_length=7, polyorder=3)

    # SG might violate the boundaries. clip them:
    SG[SG > 1 ] = 1
    SG[SG < -1 ] = -1

    ax.plot(raw_dt['human_system_start_time'], raw_dt[idx], 
            '-', label="raw", linewidth=3.5, color='red', alpha=0.4)

    ax.plot(a_df['human_system_start_time'], SG,
            '-', label="SG", linewidth=3, color='dodgerblue') # , alpha=0.8

    ax.set_title(raw_dt.ID.unique()[0] + ", " + raw_dt.CropTyp.unique()[0] + ", " + raw_dt.dataset.unique()[0])
    ax.set_ylabel(idx) # , labelpad=20); # fontsize = label_FontSize,
    ax.tick_params(axis='y', which='major') #, labelsize = tick_FontSize)
    ax.tick_params(axis='x', which='major') #, labelsize = tick_FontSize) # 
    ax.legend(loc="lower right");
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.set_ylim(raw_dt[idx].min()-0.05, 1)


def plot_raw_and_regularized(raw_dt, ax, idx="NDVI", time_step_size=10):
    a_df = raw_dt.copy()

    a_regularized_TS = nc.regularize_a_field(a_df, V_idks = idx, interval_size = time_step_size)
    # a_regularized_TS_noGap = nc.fill_theGap_linearLine(a_regularized_TS.copy(), V_idx=idx)
    a_regularized_TS_noGap = nc.fill_theGap_linearLine(a_regularized_TS, V_idx=idx)

    # Smoothen by Savitzky-Golay
    SG = scipy.signal.savgol_filter(a_regularized_TS_noGap[idx].values, window_length=7, polyorder=3)

    # SG might violate the boundaries. clip them:
    SG[SG > 1 ] = 1
    SG[SG < -1 ] = -1

    ax.plot(raw_dt['human_system_start_time'], raw_dt[idx], 
    	    '-', label="raw", linewidth=3.5, color='red', alpha=0.4)

    # ax.plot(a_regularized_TS['human_system_start_time'], 
    #         a_regularized_TS[idx], 
    #         '-.', label="regularized", linewidth=1, color='red')

    # ax.plot(a_regularized_TS_noGap['human_system_start_time'], 
    #         a_regularized_TS_noGap[idx],
    #         '-', label="no gap", linewidth=3, color='k')

    ax.plot(a_regularized_TS_noGap['human_system_start_time'], SG,
            '-', label="SG", linewidth=3, color='dodgerblue') # , alpha=0.8

    ax.set_title(raw_dt.ID.unique()[0] + ", " + raw_dt.CropTyp.unique()[0] + ", " + raw_dt.dataset.unique()[0])
    ax.set_ylabel(idx) # , labelpad=20); # fontsize = label_FontSize,
    ax.tick_params(axis='y', which='major') #, labelsize = tick_FontSize)
    ax.tick_params(axis='x', which='major') #, labelsize = tick_FontSize) # 
    ax.legend(loc="lower right");
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.set_ylim(raw_dt[idx].min()-0.05, 1)



def plot_oneColumn(raw_dt, ax, idx="NDVI", _label = "raw", _color="red"):

    ax.plot(raw_dt['human_system_start_time'], raw_dt[idx], '-', 
            label=_label, linewidth=3.5, color=_color, alpha=0.8)

    ax.set_title(raw_dt.ID.unique()[0] + ", " + raw_dt.CropTyp.unique()[0])
    ax.set_ylabel(idx) # , labelpad=20); # fontsize = label_FontSize,
    ax.tick_params(axis='y', which='major') #, labelsize = tick_FontSize)
    ax.tick_params(axis='x', which='major') #, labelsize = tick_FontSize) # 
    ax.legend(loc="lower right");
    # ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.set_ylim(raw_dt[idx].min()-0.05, 1)


