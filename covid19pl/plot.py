#!/usr/bin/env python3
# -*- coding: 'utf-8' -*-

__author__      = "oscarsierraproject.eu"
__copyright__   = "Copyright 2020, oscarsierraproject.eu"
__license__     = "GNU General Public License 3.0"
__date__        = "28th November 2020"
__maintainer__  = "oscarsierraproject.eu"
__email__       = "oscarsierraproject@protonmail.com"
__status__      = "Development"

from datetime import datetime
import logging
from matplotlib import pyplot as plt
import os
import pandas as pd
from typing import Any, Dict, List

def plot_summary_data(data: Dict[str, pd.DataFrame], workspace:str) ->None:
    """ Create a plots showing summary of gathered data """
    df_polska = pd.DataFrame()
    province = {"index": [], "values": []}
    for loc, dataframe in data.items():
        if loc == "POLSKA":
            df_polska = dataframe
            # According to stat.gov.pl Poland has 38354 thousand people
            df_polska['NC_per_100k'] = df_polska["total"].div(38354000/100000)
            df_polska['NC_per_100k_SMA_7'] = df_polska["NC_per_100k"].rolling(window=7).mean()
            df_polska['NC_SMA_7'] = df_polska["total"].rolling(window=7).mean()
            df_polska['NC_SMA_14'] = df_polska["total"].rolling(window=14).mean()
            df_polska['NC_SMA_21'] = df_polska["total"].rolling(window=21).mean()
        else:
            province["index"].append(loc)
            province["values"].append(dataframe.iloc[-1]["total"])
    df_polska.reset_index(inplace=True,drop=True)

    # Prepare the plot depending on the size of dataframe
    if df_polska.size / 300 < 1:
        plot_width = 7
    elif df_polska.size / 300 < 2:
        plot_width = 10
    else:
        plot_width = 15

    # Set plot layout
    fig, ax = plt.subplots(nrows=4, ncols=1, sharex=False)
    fig.set_size_inches(plot_width,16)
    ax[0].set_title(f"COVID19 cases in Poland {datetime.now()}\n")

    # Prepare 1st plot: Safety rules thresholds
    ax[0].plot( df_polska.index,
                df_polska["NC_per_100k"],
                color="black", marker='.', linestyle='none',
                label="New cases per 100k citizens")
    ax[0].plot( df_polska.index,
                df_polska["NC_per_100k_SMA_7"],
                color="black", marker=',', linestyle='solid',
                label="New cases per 100k citizens, SMA7")
    ax[0].set_xticks(df_polska.index)
    ax[0].set_xticklabels(df_polska["date"])
    for l in ax[0].get_xticklabels():
        l.set_rotation(90)
    if plot_width >= 15:
        # Show label on every week
        for idx, xlabel_i in enumerate(ax[0].axes.get_xticklabels()):
            if idx % 7 != 0:
                xlabel_i.set_visible(False)
                xlabel_i.set_fontsize(0.0)
    ax[0].set_ylabel("NUMBER OF NEW INFECTIONS\nPER 100k CITIZENS")
    ax[0].set_xlim(xmin=0)
    ax[0].set_ylim(ymin=0)
    ax[0].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[0].legend()
    ax[0].annotate ("%.2f"% df_polska["NC_per_100k_SMA_7"].iloc[-1],
                            ( df_polska.index[-1],
                              df_polska["NC_per_100k_SMA_7"].iloc[-1]),
                            textcoords="offset points",
                            color='black',
                            xytext=(15, 0), ha='center')
    ax[0].axhspan(0, 10, facecolor='green', alpha=0.5)
    ax[0].axhspan(10, 25, facecolor='yellow', alpha=0.5)
    ax[0].axhspan(25, 50, facecolor='red', alpha=0.5)
    ax[0].axhspan(50, 70, facecolor='violet', alpha=0.5)
    ax[0].axhspan(70, 150, facecolor='grey', alpha=0.5)

    # Prepare 2nd plot: TOTAL CASES REPORTED ----------------------------------
    ax[1].plot( df_polska.index,
                df_polska["total_sum"],
                color="red", marker=',', linestyle='solid',
                label="Cała Polska")
    ax[1].set_xticks(df_polska.index)
    ax[1].set_xticklabels(df_polska["date"])
    for l in ax[1].get_xticklabels():
        l.set_rotation(90)
    if plot_width >= 15:
        # Show label on every week
        for idx, xlabel_i in enumerate(ax[1].axes.get_xticklabels()):
            if idx % 7 != 0:
                xlabel_i.set_visible(False)
                xlabel_i.set_fontsize(0.0)
    ax[1].set_ylabel("TOTAL CASES REPORTED")
    ax[1].set_xlim(xmin=0)
    ax[1].set_ylim(ymin=0)
    ax[1].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[1].legend()
    ax[1].annotate ("%.0f"% df_polska["total_sum"].iloc[-1],
                            ( df_polska.index[-1],
                              df_polska["total_sum"].iloc[-1]),
                            textcoords="offset points",
                           xytext=(5, -10), ha='center')

    # Prepare 3rd plot: NUMBER OF NEW INFECTIONS ------------------------------
    ax[2].plot( df_polska.index,
                df_polska["total"],
                color="black", marker='.', linestyle='none',
                label="New cases")
    ax[2].plot( df_polska.index,
                df_polska["NC_SMA_7"],
                color="green", marker=',', linestyle='solid',
                label="New cases, SMA7")
    ax[2].plot( df_polska.index,
                df_polska["NC_SMA_14"],
                color="orange", marker=',', linestyle='solid',
                label="New cases, SMA14")
    ax[2].plot( df_polska.index,
                df_polska["NC_SMA_21"],
                color="magenta", marker=',', linestyle='solid',
                label="New cases, SMA21")
    ax[2].set_xticks(df_polska.index)
    ax[2].set_xticklabels(df_polska["date"])
    for l in ax[2].get_xticklabels():
        l.set_rotation(90)
    if plot_width >= 15:
        # Show label on every week
        for idx, xlabel_i in enumerate(ax[2].axes.get_xticklabels()):
            if idx % 7 != 0:
                xlabel_i.set_visible(False)
                xlabel_i.set_fontsize(0.0)
    ax[2].set_ylabel("NUMBER OF NEW INFECTIONS")
    ax[2].set_xlim(xmin=0)
    ax[2].set_ylim(ymin=0)
    ax[2].set_title("")
    ax[2].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[2].legend()
    ax[2].annotate ("%.0f"% df_polska["total"].iloc[-1],
                            ( df_polska.index[-1],
                              df_polska["total"].iloc[-1]),
                            textcoords="offset points",
                            xytext=(0, -10), ha='center')
    # Prepare 4th plot: NUMBER OF NEW INFECTIONS ------------------------------
    ax[3].plot( province["values"],
                color="purple", marker='.', linestyle='none',
                label="New cases on {}".format(df_polska["date"].iloc[-1]))
    ax[3].set_xticks(range(len(province["index"])))
    ax[3].set_xticklabels(province["index"])
    for l in ax[3].get_xticklabels():
        l.set_rotation(90)
    ax[3].set_ylabel("NEW INFECTIONS")
    ax[3].set_xlim(xmin=0)
    ax[3].set_ylim(ymin=0)
    ax[3].set_title("")
    ax[3].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[3].legend()
    for x, y in enumerate(province["values"]):
        ax[3].annotate ("%d"% y, (x, y),
                                textcoords="offset points",
                                xytext=(0, -10), ha='center')
    # Save plot in a file -----------------------------------------------------
    plot_file = os.path.join(workspace, "covid19pl.png")
    fig.savefig(plot_file)
    print("Saving plot into a file %s" % (plot_file, ))
