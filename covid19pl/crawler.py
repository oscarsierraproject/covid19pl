#!/usr/bin/env python3
# -*- coding: 'utf-8' -*-

__author__      = "oscarsierraproject.eu"
__copyright__   = "Copyright 2020, oscarsierraproject.eu"
__license__     = "GNU General Public License 3.0"
__date__        = "25nd March 2020"
__maintainer__  = "oscarsierraproject.eu"
__email__       = "oscarsierraproject@protonmail.com"
__status__      = "Development"


from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging
import os
import urllib.request

from entities import LocationEntity, LocationsLibrary
from serializers import CovidJsonEncoder

class Covid19DataCrawler(object):
    """ Web crawler gathering and storing data from gov.pl website. """

    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def __init__(self):
        self.logger         = logging.getLogger(self.__class__.__name__)

    def save_data_in_file(self, save_dir="") -> None:
        """ Store gathered data in a file in JSON format """
        if save_dir == "":
            save_dir = os.path.dirname( os.path.abspath(__file__) )
        elif not os.path.isdir( save_dir ):
            msg = "Directory '%s' does not exist" % save_dir
            self.logger.error(msg)
            raise ValueError(msg)
        f_name = "COVID19_PL_%s.json" %\
                 ( datetime.now().strftime("%s" % (self.DATE_FORMAT) ) )
        dump_data = json.dumps( self.get_data_from_gov_pl(),
                                cls=CovidJsonEncoder,
                                indent=2)
        self.logger.info("Dumping latest COVID19 data to file %s" % (f_name, ))
        with open(os.path.join(save_dir, f_name), 'w') as f:
            f.write(dump_data)

    def get_data_from_gov_pl(self) -> LocationsLibrary:
        """ Gather latest COVID19 data from www.gov.pl. """

        library = LocationsLibrary()
        url = "https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2"
        self.logger.info("Gathering Polish COVID19 data ...")
        web_url  = urllib.request.urlopen( url )
        if web_url.getcode() != 200:
            msg = "Code %s while opening %s" % (web_url.getcode(), url)
            self.logger.critical(msg)
            raise urllib.error.HTTPError(msg)
        # Gathering data is divided into steps:
        # 1. Gathering "registerData" from a web page
        # 2. Extract JSON data, 'parsedData', from gathered sample
        bs = BeautifulSoup(web_url.read(), 'html.parser')
        _reg_data = json.loads( bs.find(id="registerData").text
                                                          .replace("'", "\""))
        _parsed_data = json.loads(_reg_data['parsedData'])
        for data in _parsed_data:
            """ On March 23rd 2020 there was an issue with data on gov.pl
            website. Empty records with no data were added, as well as some 
            strange links. If bellow was introduced to deal with corrupted data
            """
            if "https" in data["Województwo"] or data["Województwo"] == "":
                continue
            l = LocationEntity( province = data['Województwo'],
                                total    = int(data['Liczba']),
                                dead     = int(data['Liczba zgonów'])\
                                           if data['Liczba zgonów'] != ''\
                                           else 0)
            library.items.append(l)
        library.items = sorted(library.items)
        self.logger.debug("Gathering Polish COVID19 data complete")
        return library
