#!/usr/bin/env python3
# -*- coding: 'utf-8' -*-

__author__      = "oscarsierraproject.eu"
__copyright__   = "Copyright 2020, oscarsierraproject.eu"
__license__     = "GNU General Public License 3.0"
__date__        = "25th March 2020"
__maintainer__  = "oscarsierraproject.eu"
__email__       = "oscarsierraproject@protonmail.com"
__status__      = "Development"

import email.message
from email.mime.text import MIMEText
import logging
import os
import pandas as pd
import smtplib
from typing import List

from entities import LocationEntity, LocationsLibrary
from serializers import CovidJsonDecoder

class Covid19HistoryContainer(object):
    """ Iterable container holding all gathered SARS-CoV-2 data """

    def __init__(self) -> None:
        self._idx:int = 0
        self._size:int = 0
        self._history: List[LocationsLibrary] = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def __iter__(self) -> object:
        return self

    def __next__(self) -> LocationsLibrary:
        if self._idx >= self._size:
            self._idx = 0
            raise StopIteration
        else:
            self._idx = self._idx + 1
            return self._history[self._idx-1]

    def add_history_data(self, data:LocationsLibrary) -> None:
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

    def get_history(self) -> List[LocationsLibrary]:
        """ Return a copy of collected history"""
        return self._history[::]

    def to_csv(self) -> None:
        """ Save collected data in CSV file """
        f_name = os.path.join( os.path.dirname( os.path.abspath(__file__) ),
                                    "data/covid19pl.csv")
        msg = f"Saving data in CSV file: {f_name}"
        print(msg)
        self.logger.info(msg)
        self.to_dataframe().to_csv(f_name)
        return None
            
    def to_dataframe(self) -> pd.DataFrame:
        """ Return collected data in form of Pandas DataFrame 
        
            Example format:
                Date,   Type,   Province_1, ..., Province_N 
            0   str ,   str,    int,      , ..., int
            1   str ,   str,    int,      , ..., int
            ...
        """ 
        _final = pd.DataFrame()
        for loc_lib in self.get_history():
            date_str = loc_lib.date.strftime("%Y-%m-%d %H:%M:%S")
            _columns        = [ "Date", "Type", ]
            _values_dead    = [ date_str, "dead"]
            _values_recover = [ date_str, "recovered"]
            _values_total   = [ date_str, "total"]
            for loc in loc_lib.items:
                _columns.append( loc.province )
                _values_dead.append( loc.dead )
                _values_recover.append( loc.recovered )
                _values_total.append( loc.total )
            _dead_df    = pd.DataFrame( [_values_dead, ], columns=_columns,) 
            _recover_df = pd.DataFrame( [_values_recover, ], columns=_columns,) 
            _total_df   = pd.DataFrame( [_values_total, ], columns=_columns,) 
            _final      = _final.append(_dead_df, ignore_index=True)
            _final      = _final.append(_recover_df, ignore_index=True)
            _final      = _final.append(_total_df, ignore_index=True)
        return _final

    def load_data_from_files(self, save_dir:str="")->None:
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
                self.add_history_data(decoder.decode(_j_data))

    def send_summary_email(self, recipient):
        """ Send email with summary data """
        SRV_ADDR    = os.getenv("EMAIL_SMTP_SRV_ADDR")
        SRV_PORT    = os.getenv("EMAIL_SMTP_SRV_PORT")
        SRV_LOGIN   = os.getenv("EMAIL_SMTP_SRV_LOGIN")
        SRV_PWD     = os.getenv("EMAIL_SMTP_SRV_PASSWORD")

        if None in [SRV_ADDR, SRV_PORT, SRV_LOGIN, SRV_PWD]:
            msg = "Unable to send email, no SMTP server configuration provided"
            self.logger.error(msg)
            return

        TEXT = ["Summary of COVID19 cases in Poland.",
                "LEGEND: Value in '()' is a ONE day difference.",
                ""]
        for idx in range(len(self._history[-1].items)):
            TEXT.append( self._get_summary_in_sentence_format( self._history[-1],
                                                               self._history[-2],
                                                               idx)
                              )
        payload = "\n".join(TEXT)

        # Prepare actual message
        msg = email.message.EmailMessage()
        msg['From'] = SRV_LOGIN
        msg['To'] = recipient if isinstance(email, list) else recipient
        msg['Subject'] = "Report: COVID19 cases in Poland"
        msg.add_header('Content-Type', 'text')
        msg.set_content( payload )
        try:
            server = smtplib.SMTP( SRV_ADDR, SRV_PORT )
            server.ehlo()
            server.starttls()
            server.login( SRV_LOGIN, SRV_PWD )
            server.send_message(msg)
            server.close()
            self.logger.info('Successfully sent mail to %s' % msg["To"])
        except Exception as err:
            print(err)
            self.logger.error("Failed to send mail to %s" % msg["To"])
            raise err

    def print_summary_data(self) -> None:
        """ Display actual summary data and 1 day change. """
        if self._size == 1:
            msg = "No historical SARS-CoV-2 data. Skipping change calculation."
            self.logger.warning( msg )
        else:
            msg = "SARS-CoV-2 data with 1 day change summary"
        print(  msg )
        print(  "%-20s: %7s %7s %7s %8s %7s %7s %7s" % \
                ("Location", "Total", "Death", "Cured",
                 "CHANGE:", "Total", "Death", "Cured")
             )
        for idx in range(len(self._history[-1].items)):
            if self._size == 1:
                print(self._history[-1].items[idx])
            else:
                print( self._get_summary_in_table_format(   self._history[-1],
                                                            self._history[-2],
                                                            idx
                            )
                )
        print(  "TIMESTAMP OF SAMPLES %s" % \
                self._history[-1].date.strftime("%Y-%m-%d %H:%M:%S"))

    def _get_summary_in_sentence_format(self,  new:LocationsLibrary,
                                            old:LocationsLibrary,
                                            idx:int) -> str:
        """ Create sentence with summary and diff between 'new' and 'old' data"""
        if new.items[idx].province != old.items[idx].province:
            raise ValueError("Province does not match")
        _d_dead    = new.items[idx].dead - old.items[idx].dead
        _d_recover = new.items[idx].recovered - old.items[idx].recovered
        _d_total   = new.items[idx].total  - old.items[idx].total
        text = "%s: %d(%d) cases, %d(%d) dead, %d(%d) recovered."%\
                (   new.items[idx].province.upper(),
                    new.items[idx].total,
                    _d_total,
                    new.items[idx].dead,
                    _d_dead,
                    new.items[idx].recovered,
                    _d_recover)
        return text

    def _get_summary_in_table_format(self,  new:LocationsLibrary,
                                            old:LocationsLibrary,
                                            idx:int) -> str:
        """ Create table with summary and diff between 'new' and 'old' data"""
        if new.items[idx].province != old.items[idx].province:
            raise ValueError("Province does not match")
        _d_dead    = new.items[idx].dead - old.items[idx].dead
        _d_recover = new.items[idx].recovered - old.items[idx].recovered
        _d_total   = new.items[idx].total  - old.items[idx].total
        text = "%-20s: %7d %7d %7d %8s %7d %7d %7d" %\
                (   new.items[idx].province,
                    new.items[idx].total,
                    new.items[idx].dead,
                    new.items[idx].recovered,
                    "",
                    _d_total,
                    _d_dead,
                    _d_recover)
        return text
