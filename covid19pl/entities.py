from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List


__author__      = "oscarsierraproject.eu"
__copyright__   = "Copyright 2020, oscarsierraproject.eu"
__license__     = "GNU General Public License 3.0"
__date__        = "25th March 2020"
__maintainer__  = "oscarsierraproject.eu"
__email__       = "oscarsierraproject@protonmail.com"
__status__      = "Development"

class BaseEntity():
    """ Base entity for all other entities """

    VERSION:    str = "1.0.0"   # Entities MUST be versioned to provide option
                                # for future improvements. Change in entity
                                # content may impact JSON handlers.


@dataclass(frozen=True)
class LocationEntity(BaseEntity):
    """ Class holding single SARS-CoV-2 province data """

    province:       str
    total:          int = 0
    total_per_10k:  float = 0 # Field added 24.11.2020
    dead:           int = 0
    recovered:      int = 0 
    dead_by_covid:  int = 0 # Field added 24.11.2020
    dead_with_covid:int = 0 # Field added 24.11.2020
    date: datetime      = datetime.now()
    VERSION:    str = "1.1.0" # Required for encoding/decoding

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

