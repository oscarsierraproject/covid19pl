#!/usr/bin/env python3
# -*- coding: 'utf-8' -*-

__author__      = "oscarsierraproject.eu"
__copyright__   = "Copyright 2020, oscarsierraproject.eu"
__license__     = "GNU General Public License 3.0"
__date__        = "26th March 2020"
__maintainer__  = "oscarsierraproject.eu"
__email__       = "oscarsierraproject@protonmail.com"
__status__      = "Development"


import logging
import optparse
import os

from crawler import Covid19DataCrawler
from entities import LocationEntity, LocationsLibrary
from history import Covid19HistoryContainer
import plot
import utils
from __version__ import __version__


# Introduction string ----------------------------------------------------------
def intro():
    print("")
    print("\tWelcome to %s in version %s" % (__file__, __version__))
    print("\tPublished on %s by %s" % (__license__, __author__))
    print("\t%s" % (__copyright__, ))
    print("\tGitHub: https://github.com/oscarsierraproject/covid19pl")
    print("")
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
    group.add_option(  "--email", action="store",
                        type="string", dest="recipient",
                        help="email address to send summary")
    group.add_option(  "--env", action="store",
                        type="string", dest="env",
                        default=os.path.join(
                                    os.path.dirname( os.path.abspath(__file__) ),
                                    ".env"),
                        help="path to file to ENV variables [default: %default]")
    group.add_option(  "--gather", action="store_true", dest="gather",
                        help="Use this option to gather latest data from gov.pl")
    group.add_option(  "--plot", action="store_true", dest="plot",
                        help="Create a plots from gathered data")
    group.add_option(  "--workspace", action="store",
                        type="string", dest="workspace",
                        default=os.path.join(
                                    os.path.dirname( os.path.abspath(__file__)),
                                    "data"),
                        help="path to directory with data [default: %default]")
    parser.add_option_group(group)
    (options, args) = parser.parse_args()
    if not options.workspace or not os.path.isdir(options.workspace):
        parser.error("Data directory does not exist or was not provided.\n\n"\
                     "See --help for more details.")
    return options
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    intro()
    root_logger = utils.setup_root_logger()
    options     = parse_options()
    # Proper order of options handling: debug -> env -> gather -> display
    if options.debug:
        # Drop down logging level to DEBUG for all handlers
        root_logger.setLevel(logging.DEBUG)
        for h in root_logger.handlers:
            h.setLevel(logging.DEBUG)
    if options.recipient and options.env:
        root_logger.info("Loading environment variables from %s"%\
                         (options.env,) )
        utils.load_env_variables( options.env)
    if options.gather:
        # Gather latest data from www.gov.pl
        covid19_web_crawler = Covid19DataCrawler()
        covid19_web_crawler.save_data_in_file( options.workspace )
    covid19_history = Covid19HistoryContainer()
    covid19_history.load_data_from_files( options.workspace )
    if options.display:
        covid19_history.print_summary_data()
    if options.recipient:
        covid19_history.send_summary_email( options.recipient )
    if options.plot:
        plot.plot_summary_data(covid19_history, options.workspace)
