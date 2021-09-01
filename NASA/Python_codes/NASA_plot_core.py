import matplotlib.pyplot as plt
import seaborn as sb
import sys
import scipy
import scipy.signal
import matplotlib.dates as mdates
sys.path.append('/Users/hn/Documents/00_GitHub/Ag/NASA/Python_codes/')
import NASA_core as nc


def plot_8dayComposite_and_SG(raw_dt, ax, idx="NDVI", time_step_size=10):
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

