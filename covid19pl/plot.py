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
    _plot_areas_df = df[df["Type"]=="total"]
    _plot_areas_df = _plot_areas_df.loc[_plot_areas_df.index[-2]:
                                        _plot_areas_df.index[-1],
                                       [  "dolnośląskie",
                                          "kujawsko-pomorskie",
                                          "lubelskie",
                                          "lubuskie",
                                          "mazowieckie",
                                          "małopolskie",
                                          "opolskie",
                                          "podkarpackie",
                                          "podlaskie",
                                          "pomorskie",
                                          "warmińsko-mazurskie",
                                          "wielkopolskie",
                                          "zachodniopomorskie",
                                          "łódzkie",
                                          "śląskie",
                                          "świętokrzyskie"]
                                        ]
    _plot_areas_series = _plot_areas_df.diff().iloc[-1]
    # Create data structure for all tracked provinces -------------------------
    _plot_df = df[ df["Type"]=="total"][ ["Date", "Cała Polska",] ]
    _plot_df = _plot_df.reset_index(drop=True)
    _timestamp = _plot_df.at[ _plot_df.index[-1], "Date"]
    # Strip data to keep only day and month value
    _plot_df["Date"] = _plot_df["Date"].map(lambda x: x[5:10:])
    _plot_df["New cases"] = _plot_df["Cała Polska"].diff()
    # According to stat.gov.pl Poland has 38354 thousand people """
    _plot_df['NC_per_100k'] = _plot_df["New cases"].div(38354000/100000)
    _plot_df['NC_per_100k_SMA_7'] = _plot_df["NC_per_100k"].rolling(window=7).mean()
    _plot_df['NC_SMA_7'] = _plot_df["New cases"].rolling(window=7).mean()
    _plot_df['NC_SMA_14'] = _plot_df["New cases"].rolling(window=14).mean()
    _plot_df['NC_SMA_21'] = _plot_df["New cases"].rolling(window=21).mean()
    #_plot_df["New cases %"] = _plot_df["New cases"]/_plot_df["Cała Polska"]*100
    # Prepare the plot
    fig, ax = plt.subplots(nrows=4, ncols=1, sharex=False)
    fig.set_size_inches(15,15)
    ax[0].set_title(f"COVID19 cases in Poland\nSamples timestamp: {_timestamp}")
    # Prepare 1st plot: Safety rules thresholds
    ax[0].plot( _plot_df["Date"],
                _plot_df["NC_per_100k"],
                color="black", marker='.', linestyle='none',
                label="New cases per 100k citizens")
    ax[0].plot( _plot_df["Date"],
                _plot_df["NC_per_100k_SMA_7"],
                color="black", marker=',', linestyle='solid',
                label="New cases per 100k citizens, SMA7")
    # Show label on every week
    for idx, xlabel_i in enumerate(ax[0].axes.get_xticklabels()):
        if idx % 7 != 0:
            xlabel_i.set_visible(False)
            xlabel_i.set_fontsize(0.0)
    ax[0].set_xticks(_plot_df["Date"])
    for l in ax[0].get_xticklabels():
        l.set_rotation(90)
    ax[0].set_ylabel("NUMBER OF NEW INFECTIONS\nPER 100k CITIZENS")
    ax[0].set_xlim(xmin=0)
    ax[0].set_ylim(ymin=0)
    ax[0].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[0].legend()
    ax[0].annotate ("%.3f"% _plot_df["NC_per_100k_SMA_7"].iloc[-1],
                            ( _plot_df["Date"].iloc[-1],
                              _plot_df["NC_per_100k_SMA_7"].iloc[-1]),
                            textcoords="offset points",
                            color='black',
                            xytext=(0, 5), ha='center')
    ax[0].axhspan(0, 10, facecolor='green', alpha=0.5)
    ax[0].axhspan(10, 25, facecolor='yellow', alpha=0.5)
    ax[0].axhspan(25, 50, facecolor='red', alpha=0.5)
    ax[0].axhspan(50, 75, facecolor='violet', alpha=0.5)
    ax[0].axhspan(75, 150, facecolor='grey', alpha=0.5)
    # Prepare 2nd plot: TOTAL CASES REPORTED ----------------------------------
    ax[1].plot( _plot_df["Date"],
                _plot_df["Cała Polska"],
                color="red", marker=',', linestyle='solid',
                label="Cała Polska")
    # Show label on every week
    for idx, xlabel_i in enumerate(ax[1].axes.get_xticklabels()):
        if idx % 7 != 0:
            xlabel_i.set_visible(False)
            xlabel_i.set_fontsize(0.0)
    for l in ax[1].get_xticklabels():
        l.set_rotation(90)
    ax[1].set_ylabel("TOTAL CASES REPORTED")
    ax[1].set_xlim(xmin=0)
    ax[1].set_ylim(ymin=0)
    ax[1].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[1].legend()
    ax[1].annotate ("%.0f"% _plot_df["Cała Polska"].iloc[-1],
                            ( _plot_df["Date"].iloc[-1],
                              _plot_df["Cała Polska"].iloc[-1]),
                            textcoords="offset points",
                           xytext=(0, 5), ha='center')
    # Prepare 3rd plot: NUMBER OF NEW INFECTIONS ------------------------------
    ax[2].plot( _plot_df["Date"],
                _plot_df["New cases"],
                color="black", marker='.', linestyle='none',
                label="New cases")
    ax[2].plot( _plot_df["Date"],
                _plot_df["NC_SMA_7"],
                color="green", marker=',', linestyle='solid',
                label="New cases, SMA7")
    ax[2].plot( _plot_df["Date"],
                _plot_df["NC_SMA_14"],
                color="orange", marker=',', linestyle='solid',
                label="New cases, SMA14")
    ax[2].plot( _plot_df["Date"],
                _plot_df["NC_SMA_21"],
                color="magenta", marker=',', linestyle='solid',
                label="New cases, SMA21")
    # Show label on every week
    for idx, xlabel_i in enumerate(ax[2].axes.get_xticklabels()):
        if idx % 7 != 0:
            xlabel_i.set_visible(False)
            xlabel_i.set_fontsize(0.0)
    ax[2].set_xticks(_plot_df["Date"])
    for l in ax[2].get_xticklabels():
        l.set_rotation(90)
    ax[2].set_ylabel("NUMBER OF NEW INFECTIONS")
    ax[2].set_xlim(xmin=0)
    ax[2].set_ylim(ymin=0)
    ax[2].set_title("")
    ax[2].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[2].legend()
    ax[2].annotate ("%.0f"% _plot_df["New cases"].iloc[-1],
                            ( _plot_df["Date"].iloc[-1],
                              _plot_df["New cases"].iloc[-1]),
                            textcoords="offset points",
                            xytext=(0, 5), ha='center')

    # Prepare 4th plot: NUMBER OF NEW INFECTIONS ------------------------------
    ax[3].plot( _plot_areas_series,
                color="purple", marker='1', linestyle='none',
                label="New cases on {}".format(_plot_df["Date"].iloc[-1]))
    ax[3].set_xticks(_plot_areas_series.index)
    for l in ax[3].get_xticklabels():
        l.set_rotation(90)
    ax[3].set_ylabel("NEW INFECTIONS")
    ax[3].set_xlim(xmin=0)
    ax[3].set_ylim(ymin=0)
    ax[3].set_title("")
    ax[3].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[3].legend()
    for x, y in enumerate(_plot_areas_series.values):
        ax[3].annotate ("%d"% y, (x, y),
                                textcoords="offset points",
                                xytext=(0, 5), ha='center')
    # Save plot in a file -----------------------------------------------------
    plot_file = os.path.join(workspace, "covid19pl.png")
    fig.savefig(plot_file)
    print("Saving plot into a file %s" % (plot_file, ))
