#!/usr/bin/env python3
# -*- coding: 'utf-8' -*-

__author__      = "oscarsierraproject.eu"
__copyright__   = "Copyright 2020, oscarsierraproject.eu"
__license__     = "GNU General Public License 3.0"
__date__        = "26th March 2020"
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
    _plot_df["change"] = _plot_df["Cała Polska"].diff()
    
    # Prepare the plot
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=False)
    fig.set_size_inches(15,15)
    # Prepare 1st plot: TOTAL CASES REPORTED ----------------------------------
    ax[0].plot( _plot_df["Date"],
                _plot_df["Cała Polska"],
                color="red", marker='o', linestyle='dashed', 
                label="Cała Polska")
    for l in ax[0].get_xticklabels():
        l.set_rotation(90)
    ax[0].set_ylabel("TOTAL CASES REPORTED")
    ax[0].set_xlim(xmin=0)
    ax[0].set_ylim(ymin=0)
    ax[0].set_title(f"COVID19 cases in Poland\nSamples timestamp: {_timestamp}")
    ax[0].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[0].legend()
    for x, y in zip(_plot_df["Date"], _plot_df["Cała Polska"]):
        ax[0].annotate ("%.0f"%y, (x, y), textcoords="offset points",
                                          xytext=(0, 5), ha='center')
    # Prepare 2nd plot: NUMBER OF NEW INFECTIONS ------------------------------
    ax[1].plot( _plot_df["Date"],
                _plot_df["change"],
                color="grey", marker='o', linestyle='dashed',
                label="Cała Polska")
    ax[1].set_xticks(_plot_df["Date"])
    for l in ax[1].get_xticklabels():
        l.set_rotation(90)
    ax[1].set_ylabel("NUMBER OF NEW INFECTIONS")
    ax[1].set_xlim(xmin=0)
    ax[1].set_ylim(ymin=0)
    ax[1].set_title("")
    ax[1].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[1].legend()
    for x, y in zip(_plot_df["Date"], _plot_df["change"]):
        ax[1].annotate ("%.0f"%y, (x, y), textcoords="offset points", 
                                          xytext=(0, 5), ha='center')
    # Save plot in a file -----------------------------------------------------
    plot_file = os.path.join(workspace, "covid19pl.png")
    fig.savefig(plot_file)
    print("Saving plot into a file %s" % (plot_file, ))
