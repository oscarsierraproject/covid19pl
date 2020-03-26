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
import json
import logging
import logging.config
from typing import Any, List
from entities import LocationEntity, LocationsLibrary

class CovidJsonDecoder(json.JSONDecoder):
    """ JSON data decoder prepared to handle specific COVID19 JSON data. """

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(CovidJsonDecoder, self).__init__( object_hook=self.object_hook,
                                                *args)

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
                      "value": obj.strftime( "%s %s"% ( self.DATE_FORMAT,
                                                        self.TIME_FORMAT)) }
        else:
            raise ValueError("Not supported object type")
