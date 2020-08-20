#!/usr/bin/env python3
# -*- coding: 'utf-8' -*-

__author__      = "oscarsierraproject.eu"
__copyright__   = "Copyright 2020, oscarsierraproject.eu"
__license__     = "GNU General Public License 3.0"
__date__        = "10th April 2020"
__maintainer__  = "oscarsierraproject.eu"
__email__       = "oscarsierraproject@protonmail.com"
__status__      = "Development"

from datetime import datetime
import logging
from matplotlib import pyplot as plt
import os
import pandas as pd
from typing import Any, List
from entities import LocationEntity, LocationsLibrary
from history import Covid19HistoryContainer
import utils

def plot_summary_data(df: pd.DataFrame, workspace:str) ->None:
    """ Create a plots showing summary of gathered data """

    # Create data structure for all tracked provinces -------------------------
    _plot_df = df[ df["Type"]=="total"][ ["Date", "Cała Polska",] ]
    _plot_df = _plot_df.reset_index(drop=True)
    _timestamp = _plot_df.at[ _plot_df.index[-1], "Date"]
    # Strip data to keep only day and month value
    _plot_df["Date"] = _plot_df["Date"].map(lambda x: x[5:10:])
    _plot_df["New cases"] = _plot_df["Cała Polska"].diff()
    _plot_df["New cases %"] = _plot_df["New cases"]/_plot_df["Cała Polska"]*100
    # Prepare the plot
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=False)
    fig.set_size_inches(15,15)
    # Prepare 1st plot: TOTAL CASES REPORTED ----------------------------------
    ax[0].plot( _plot_df["Date"],
                _plot_df["Cała Polska"],
                color="red", marker='.', linestyle='solid',
                label="Cała Polska")
    # Show label on every week
    for idx, xlabel_i in enumerate(ax[0].axes.get_xticklabels()):
        if idx % 7 != 0:
            xlabel_i.set_visible(False)
            xlabel_i.set_fontsize(0.0)
    for l in ax[0].get_xticklabels():
        l.set_rotation(90)
    ax[0].set_ylabel("TOTAL CASES REPORTED")
    ax[0].set_xlim(xmin=0)
    ax[0].set_ylim(ymin=0)
    ax[0].set_title(f"COVID19 cases in Poland\nSamples timestamp: {_timestamp}")
    ax[0].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[0].legend()
    ax[0].annotate ("%.0f"% _plot_df["Cała Polska"].iloc[-1],
                            ( _plot_df["Date"].iloc[-1],
                              _plot_df["Cała Polska"].iloc[-1]),
                            textcoords="offset points",
                           xytext=(0, 5), ha='center')
    # Prepare 2nd plot: NUMBER OF NEW INFECTIONS ------------------------------
    ax[1].plot( _plot_df["Date"],
                _plot_df["New cases"],
                color="grey", marker='o', linestyle='dashed',
                label="Cała Polska")
    # Show label on every week
    for idx, xlabel_i in enumerate(ax[1].axes.get_xticklabels()):
        if idx % 7 != 0:
            xlabel_i.set_visible(False)
            xlabel_i.set_fontsize(0.0)
    ax[1].set_xticks(_plot_df["Date"])
    for l in ax[1].get_xticklabels():
        l.set_rotation(90)
    ax[1].set_ylabel("NUMBER OF NEW INFECTIONS")
    ax[1].set_xlim(xmin=0)
    ax[1].set_ylim(ymin=0)
    ax[1].set_title("")
    ax[1].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[1].legend()
    ax[1].annotate ("%.0f"% _plot_df["New cases"].iloc[-1],
                            ( _plot_df["Date"].iloc[-1],
                              _plot_df["New cases"].iloc[-1]),
                            textcoords="offset points",
                            xytext=(0, 5), ha='center')
    # Prepare 2nd plot: NUMBER OF NEW INFECTIONS ------------------------------
    """
    ax[2].plot( _plot_df["Date"],
                _plot_df["New cases %"],
                color="blue", marker='o', linestyle='dashed',
                label="Cała Polska")
    ax[2].set_xticks(_plot_df["Date"])
    for l in ax[2].get_xticklabels():
        l.set_rotation(90)
    ax[2].set_ylabel("NEW INFECTIONS / TOTAL INFECTIONS * 100")
    ax[2].set_xlim(xmin=0)
    ax[2].set_ylim(ymin=0)
    ax[2].set_ylim(ymax=110)
    ax[2].set_title("")
    ax[2].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[2].legend()
    ax[2].annotate ("%.1f"% _plot_df["New cases %"].iloc[-1],
                            ( _plot_df["Date"].iloc[-1],
                              _plot_df["New cases %"].iloc[-1]),
                            textcoords="offset points",
                            xytext=(0, 5), ha='center')
    """
    # Save plot in a file -----------------------------------------------------
    plot_file = os.path.join(workspace, "covid19pl.png")
    fig.savefig(plot_file)
    print("Saving plot into a file %s" % (plot_file, ))
