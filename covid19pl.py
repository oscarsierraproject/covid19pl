#!/usr/bin/env python3
# -*- coding: 'utf-8' -*-

__author__      = "oscarsierraproject.eu"
__copyright__   = "Copyright 2020, oscarsierraproject.eu"
__license__     = "GNU General Public License 3.0"
__version__     = "1.1.0"
__date__        = "21st March 2020"
__maintainer__  = "oscarsierraproject.eu"
__email__       = "oscarsierraprojectk@protonmail.com"
__status__      = "Production"


from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
import logging.config
import optparse
import os
import sys
from typing import Any, List
import urllib.request

# Introduction string ----------------------------------------------------------
def intro():
    print("")
    print("\tWelcome to %s in version %s" % (__file__, __version__))
    print("\tPublished on %s by %s" % (__license__, __author__))
    print("\t%s" % (__copyright__, ))
    print("\tGitHub: https://github.com/oscarsierraproject/covid19pl") 
    print("")
# ------------------------------------------------------------------------------ 

# Setup logging facility to improve execution readability ----------------------
logging_level  = logging.WARNING
logging_config = dict(
    version = 1,
    formatters = {
        'f': {  'format':
                '%(asctime)s | %(levelname)8s | %(message)s | %(name)10s'
        },
    },
    handlers = {
        'h': {  'class': 'logging.StreamHandler',
                'formatter': 'f',
                'level': logging_level,
        },
    },
    root = {
        'handlers': ['h'],
        'level': logging_level,
    },
)
logging.config.dictConfig(logging_config)
root_logger = logging.getLogger()   # Global for the script
# ------------------------------------------------------------------------------ 

# Setup initial options parser -------------------------------------------------
def parse_options():
    parser = optparse.OptionParser( usage = "%prog --workspace=<PATH>",
                                    version = "%prog {}".format(__version__),
                                    epilog = "{}, {}".format(__copyright__,
                                                             __license__))
    group = optparse.OptionGroup(parser, "OPTIONAL OPTIONS")
    group.add_option(  "--debug", action="store_true", dest="debug",
                        help="Run script in debug mode")
    group.add_option(  "--display", action="store_true", dest="display",
                        help="Display latest data for Poland")
    group.add_option(  "--gather", action="store_true", dest="gather",
    group.add_option(  "--workspace", action="store", 
                        type="string", dest="workspace",
                        default=os.path.join( os.path.dirname( os.path.abspath(__file__)), 
                                             "data"),
                        help="path to directory with data [default: %default]")
                        help="Use this option to gather latest data from gov.pl")
    parser.add_option_group(group)
    (options, args) = parser.parse_args()
    if not options.workspace or not os.path.isdir(options.workspace):
        parser.error("Directory with data does not exist or was not provided.\n\n"\
                     "See --help for more details.")
    return options
# ------------------------------------------------------------------------------ 


class BaseEntity():
    """ Base entity for all other entities """
    
    VERSION:    str = "1.0.0"   # Entities MUST be versioned to provide option
                                # for future improvements. Change in entity 
                                # content may impact JSON handlers.


@dataclass(frozen=True)
class LocationEntity(BaseEntity):
    """ Class holding single SARS-CoV-2 province data """

    province:   str
    total:      int = 0
    dead:       int = 0
    recovered:  int = 0
    date:       datetime = datetime.now()
    VERSION:    str = "1.0.0" # Required for encoding/decoding

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LocationEntity):
            raise NotImplementedError
        return self.province == other.province

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, LocationEntity):
            raise NotImplementedError
        return self.province > other.province

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, LocationEntity):
            raise NotImplementedError
        return self.province < other.province

    def __repr__(self):
        return "%-20s: %7d %7d %7d" % \
                (self.province, self.total, self.dead, self.recovered)

@dataclass(frozen=False)
class LocationsLibrary(BaseEntity):
    """ Data library with historical SARS-CoV-2 samples """

    VERSION: str                = "1.0.0"   # Required for encoding/decoding
    date: datetime              = datetime.now()
    items: List[LocationEntity] = field(default_factory=list)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LocationsLibrary):
            raise NotImplementedError
        return self.date == other.date

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, LocationsLibrary):
            raise NotImplementedError
        return self.date > other.date

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, LocationsLibrary):
            raise NotImplementedError
        return self.date < other.date


class CovidHistoryContainer(object):
    """ Iterable container holding all gathered SARS-CoV-2 data """

    def __init__(self) -> None:
        self._idx:int = 0
        self._size:int = 0
        self._history: list[LocationsLibrary] = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def __iter__(self) -> object:
        return self

    def __next__(self) -> LocationsLibrary:
        if self._idx >= self._size:
            self._idx = 0
            return StopIteration
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
        # WARNING: It is important to have data sorted at this stage!
        data.items.sort()
        self._history.append(data)
        self._history.sort()
        self._size = len(self._history)

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

    def print_summary_data(self) -> None:
        """ Display actual summary data and 1 day change. """
        if self._size == 1:
            msg = "No historical SARS-CoV-2 data. Skipping change calculation."
            self.logger.warning( msg )
        else:
            msg = "SARS-CoV-2 data with 1 day change summary"
        print(  msg )
        print(  "%-20s: %7s %7s %7s %8s %7s %7s %7s" % \
                ("Location", "Total", "Death", "Cured", "CHANGE:", "Total", "Death", "Cured"))
        for idx in range(len(self._history[-1].items)):
            if self._size == 1:
                print(self._history[-1].items[idx])
            else:
                print( self._get_summary_string( self._history[-1], self._history[-2], idx) )
        print(  "TIMESTAMP OF SAMPLES %s" % \
                self._history[-1].date.strftime("%Y-%m-%d %H:%M:%S"))

    def _get_summary_string(self, new:LocationsLibrary, old:LocationsLibrary, idx:int) -> str:
        """ Prepare summary line with diff between 'new' and 'old' data sample """
        if new.items[idx].province != old.items[idx].province:
            raise ValueError("Province does not match")
        _d_dead    = new.items[idx].dead - old.items[idx].dead
        _d_recover = new.items[idx].recovered - old.items[idx].recovered
        _d_total   = new.items[idx].total  - old.items[idx].total
        return("%-20s: %7d %7d %7d %8s %7d %7d %7d" %
                (   new.items[idx].province,
                    new.items[idx].total,
                    new.items[idx].dead, 
                    new.items[idx].recovered, 
                    "", 
                    _d_total, 
                    _d_dead, 
                    _d_recover))


class CovidJsonDecoder(json.JSONDecoder):
    """ JSON data decoder prepared to handle specific COVID19 JSON data. """

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(CovidJsonDecoder, self).__init__(object_hook=self.object_hook, *args)

    def object_hook(self, obj):
        if "_type" not in obj:
            return obj
        elif obj["_type"] == "LocationsLibrary":
            return LocationsLibrary(items=obj["value"]["items"], 
                                    date=obj["value"]["date"],
                                    VERSION=obj["value"]["VERSION"])
            raise NotImplementedError
        elif obj["_type"] == "LocationEntity":
            return LocationEntity(  province=obj["value"]["province"],
                                    total=int( obj["value"]["total"]),
                                    dead=int( obj["value"]["dead"]), 
                                    recovered=int( obj["value"]["recovered"] ),
                                    date=obj["value"]["date"],
                                    VERSION=obj["value"]["VERSION"])
            raise NotImplementedError
        elif obj["_type"] == "datetime": 
            return datetime.strptime( obj['value'], obj['_format'] )
        else:
            msg = "Unsupported object type '%s'" % obj["_type"]
            self.logger.error(msg)
            raise json.JSONDecoderError(msg)


class CovidJsonEncoder(json.JSONEncoder):
    """ Class serializing COVID-19 LocationsLibrary into JSON format. """

    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, obj:Any) -> str:
        if isinstance(obj, LocationsLibrary):
            _j = {}
            for k, v in obj.__dict__.items():
                _j[k] = v
            return {'_type': 'LocationsLibrary', 
                    '_version': obj.VERSION, 
                    'value': _j}
        elif isinstance(obj, LocationEntity):
            _j = {}
            for k, v in obj.__dict__.items():
                _j[k] = v
            return {'_type': 'LocationEntity', 
                    '_version': obj.VERSION, 
                    'value': _j}
        elif isinstance(obj, datetime):
            _j = {}
            return {  "_type": "datetime",
                      "_format": "%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT),
                      "value": obj.strftime( "%s %s"% (self.DATE_FORMAT, self.TIME_FORMAT)) }
        else:
            raise ValueError("Not supported object type")


class CovidDataCrawler(object):
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
        f_name = "COVID19_PL_%s.json" % ( datetime.now().strftime("%s"%(self.DATE_FORMAT) ), ) 
        dump_data = json.dumps(self.get_data_from_gov_pl(), cls=CovidJsonEncoder, indent=2)
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
        _register_data = json.loads(bs.find(id="registerData").text.replace("'", "\""))
        _parsed_data = json.loads(_register_data['parsedData']) 
        for data in _parsed_data:
            l = LocationEntity( province = data['Województwo'],
                                total    = int(data['Liczba']),
                                dead     = int(data['Liczba zgonów']) if data['Liczba zgonów'] != '' else 0)
            library.items.append(l)
        library.items = sorted(library.items)
        self.logger.debug("Gathering Polish COVID19 data complete")
        return library


if __name__ == "__main__":
    intro()
    options = parse_options()
    # Proper order of options handling: debug -> gather -> display
    if options.debug:
        # Drop down logging level to DEBUG for all handlers
        root_logger.setLevel(logging.DEBUG)
        for h in root_logger.handlers:
            h.setLevel(logging.DEBUG)
    if options.gather:
        # Gather latest data from www.gov.pl
        covid19_web_crawler = CovidDataCrawler()
        covid19_web_crawler.save_data_in_file( options.workspace )
    if options.display:
        # Process data and prepare it for display
        covid19_history = CovidHistoryContainer()
        covid19_history.load_data_from_files( options.workspace )
        covid19_history.print_summary_data()
