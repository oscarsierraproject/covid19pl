#!/usr/bin/env python3
# -*- coding: 'utf-8' -*-

__author__      = "oscarsierraproject.eu"
__copyright__   = "Copyright 2020, oscarsierraproject.eu"
__license__     = "GNU General Public License 3.0"
__date__        = "25th March 2020"
__maintainer__  = "oscarsierraproject.eu"
__email__       = "oscarsierraproject@protonmail.com"
__status__      = "Development"

from datetime import datetime
import logging
from matplotlib import pyplot as plt
import os
from typing import Any, List

from entities import LocationEntity, LocationsLibrary
from history import Covid19HistoryContainer
import utils

def get_one_day_change(samples: List) -> List:
    """ Calculate samples change rate on day interval """

    _ch_rate = []
    for x, _ in enumerate(samples):
        if samples[x] == 0:
            _ch_rate.append(0)
        elif samples[x-1] == 0:
            _ch_rate.append(samples[x]*100)
        else:
            _ch_rate.append((samples[x]-samples[x-1])/samples[x-1]*100)
    return _ch_rate

def plot_summary_data(history_container, workspace):
    """ Create a plots showing summary of gathered data """

    # Create data structure for all tracked provinces
    plot_data = {}
    for location in history_container.get_history()[0].items:
        if location.province not in plot_data.keys():
            plot_data[location.province] = {    "x": [],
                                                "xticks": [],
                                                "total": [],
                                                "dead": [],
                                                "recovered": [], }
    # Populate plot data structure with samples
    for idx, loc_lib in enumerate(history_container):
        for loc in loc_lib.items:
            plot_data[loc.province]["x"].append(idx)
            plot_data[loc.province]["xticks"].append(loc.date.strftime("%d-%m"))
            plot_data[loc.province]["total"].append(loc.total)
            plot_data[loc.province]["dead"].append(loc.dead)
            plot_data[loc.province]["recovered"].append(loc.recovered)
    # Prepare the plot
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=False)
    fig.set_size_inches(15,15)
    # Prepare 1st plot
    ax[0].plot( plot_data["Cała Polska"]["xticks"],
                plot_data["Cała Polska"]["total"],
                color="red", marker='o', linestyle='dashed', 
                label="Cała Polska")
    for l in ax[0].get_xticklabels():
        l.set_rotation(90)
    ax[0].set_ylabel("TOTAL CASES REPORTED")
    ax[0].set_xlim(xmin=0)
    ax[0].set_ylim(ymin=0)
    ax[0].set_title("COVID19 cases in Poland\nSamples timestamp: %s" %\
                 history_container._history[-1].items[0].date.strftime("%Y-%m-%d %H:%M:%S"))
    ax[0].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[0].legend()
    for x, y in zip(plot_data["Cała Polska"]["xticks"],
                    plot_data["Cała Polska"]["total"]):
        ax[0].annotate ("%.0f"%y, (x, y), textcoords="offset points", xytext=(0, 5), ha='center')
    # Prepare 2nd plot
    y_data = get_one_day_change(plot_data["Cała Polska"]["total"])
    ax[1].plot( plot_data["Cała Polska"]["xticks"],
                y_data,
                color="blue", marker='o', linestyle='dashed',
                label="Cała Polska")
    ax[1].set_xticks(plot_data["Cała Polska"]["xticks"])
    for l in ax[1].get_xticklabels():
        l.set_rotation(90)
    ax[1].set_xlabel("TIME`")
    ax[1].set_ylabel("NEW INFECTIONS / TOTAL INFECTIONS")
    ax[1].set_xlim(xmin=0)
    ax[1].set_ylim(ymin=0)
    ax[1].set_title("")
    ax[1].grid(b=True, which="both", axis="both", linestyle='dotted')
    ax[1].legend()
    for x, y in zip(plot_data["Cała Polska"]["xticks"], y_data):
        ax[1].annotate ("%.2f"%y, (x, y), textcoords="offset points", xytext=(0, 5), ha='center')
    # Save plot in a file
    plot_file = os.path.join(workspace, "covid19pl.png")
    fig.savefig(plot_file)
    print("Saving plot into a file %s" % (plot_file, ))
