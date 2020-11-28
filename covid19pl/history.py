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
import os
import pandas as pd
from typing import Dict, List

from entities import LocationEntity, LocationsLibrary
from serializers import CovidJsonDecoder

class Covid19HistoryContainer(object):
    """ Iterable container holding all gathered SARS-CoV-2 data """

    def __init__(self) -> None:
        self._idx:int = 0
        self._size:int = 0
        self._data:Dict[str, pd.DataFrame]
        self._history: List[LocationsLibrary] = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def _add_history_data(self, data:LocationsLibrary) -> None:
        """ Add data to historical data to history container.

        It is important to store data sorted at this stage, as methods
        executed later will assume that data is in order.
        """
        if not isinstance(data, LocationsLibrary):
            raise ValueError("Not compatible data type")
        # : It is important to have data sorted at this stage!
        data.items.sort()
        self._history.append(data)
        self._history.sort()
        self._size = len(self._history)

    def _move_data_dataframe(self) -> Dict[str, pd.DataFrame]:
        """ Store data into Pandas Data Frame for further use """
        data: Dict[str, pd.DataFrame] = {}
        columns = [ "date", "total", "total_per_10k",
                    "dead", "dead_by_covid", "dead_with_covid"]
        for loc_lib in self._history:
            for loc in loc_lib.items:
                if loc.province in ["Cała Polska", "Cały kraj"]:
                    province = "POLSKA"
                else:
                    province = loc.province.upper()
                if province not in data.keys():
                    data[province] = pd.DataFrame(  columns = columns)
                tmp = { "date": loc.date.date(),
                        "total": loc.total,
                        "total_per_10k": loc.total_per_10k,
                        "dead": loc.dead,
                        "dead_by_covid": loc.dead_by_covid,
                        "dead_with_covid": loc.dead_with_covid}
                data[province].loc[len(data[province].index)] = tmp

        # Make LocationEntity v. 1.0.0 and 1.1.0 data compatible
        for _, value in data.items():
            self._process_data_to_daily_values(value)
            # Verify if last record has today's data, else zero it
            if value["total"].iat[-1] == value["total"].iat[-2] and\
               value["dead"].iat[-1] == value["dead"].iat[-2]:
                value["total"].iat[-1] = 0
                value["total_per_10k"].iat[-1] = 0
                value["dead"].iat[-1] = 0
                value["dead_by_covid"].iat[-1] = 0
                value["dead_with_covid"].iat[-1] = 0
            value["total_sum"] = value["total"]\
                                .rolling(min_periods=0, window=65535)\
                                .sum()
            # TODO: Add missing people in "total_sum" which were not included
            # in previous gov.pl data:
            # - (-611) on 22.11.2020
            # - (+22594) on 24.11.2020
        return data

    def _process_data_to_daily_values(self, df: pd.DataFrame) -> None:
        """ Proces location dataframe and convert all values in it
        into a daily deltas.
        Step required due to change the way how data is being served
        on source, gov.pl, site.
        November 23, 2020 is a point where data serving was change from
        incremental into a daily deltas."""

        idx = df["date"][df["date"] == datetime(2020,11,23).date()].index[0]
        while(idx>0):
            df.total.iloc[idx] = df.total.iloc[idx] - df.total.iloc[idx-1]
            df.dead.iloc[idx] = df.dead.iloc[idx] - df.dead.iloc[idx-1]
            # df.recovered was never published so it's skipped
            idx -= 1

    def get_data_to_analyse(self) -> Dict[str, pd.DataFrame]:
        """ Return DataFrame filled with data from JSON files """
        return self._data

    def get_history(self) -> List[LocationsLibrary]:
        """ Return a copy of collected history"""
        return self._history[::]

    def load_data_from_files(self, save_dir:str="") -> None:
        """ Load JSON data from files and store it in history attribute """
        if save_dir == "":
            save_dir = os.path.dirname( os.path.abspath(__file__) )
        COVID19_files = sorted( [   os.path.join(save_dir, f) \
                                    for f in os.listdir(save_dir) \
                                    if "COVID19" in f] )
        decoder = CovidJsonDecoder()
        for f_json in COVID19_files:
            self.logger.info("Loading data from '%s'" % (f_json))
            with open(f_json, 'r') as f:
                _j_data = "".join(f.readlines())
                self._add_history_data(decoder.decode(_j_data))
        self._data = self._move_data_dataframe()

    def to_csv(self) -> None:
        """ Save collected data in CSV file """
        for loc, data in self._data.items():
            f_name = os.path.join( os.path.dirname( os.path.abspath(__file__) ),
                                        f"data/covid19pl_{loc}.csv")
            msg = f"Saving data in CSV file: {f_name}"
            print(msg)
            self.logger.info(msg)
            data.to_csv(f_name)
