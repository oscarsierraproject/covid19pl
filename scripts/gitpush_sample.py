#!/usr/bin/env python3
# -*- coding: 'utf-8' -*-

""" Script for automatic delivery of collected samples, for a current day,
    to specified remote branch."""


__author__      = "oscarsierraproject.eu"
__copyright__   = "Copyright 2020, oscarsierraproject.eu"
__license__     = "GNU General Public License 3.0"
__date__        = "26th March 2020"
__maintainer__  = "oscarsierraproject.eu"
__email__       = "oscarsierraproject@protonmail.com"
__status__      = "Development"
__version__     = "1.0.0"


from datetime import datetime
import optparse
import os
import subprocess
import sys


# Gather initial options ------------------------------------------------------
parser = optparse.OptionParser( usage = "%prog --branch --remote",
                                version = "%prog {}".format(__version__),
                                epilog = "{}, {}".format(__copyright__,
                                                         __license__))
group = optparse.OptionGroup(parser, "MANDATORY OPTIONS")
group.add_option(  "--branch", action="store", dest="branch",
                    help="branch name to push data to")
group.add_option(  "--remote", action="store", dest="remote",
                    help="remote name to push data to")
parser.add_option_group(group)
(options, args) = parser.parse_args()
if options.branch is None or options.remote is None:
    parser.error("Missing --branch and --remote specification\n\n"\
                 "See --help for more details.")

# Prepare script variables ----------------------------------------------------
BASE_DIR    = os.path.join(os.path.dirname( os.path.abspath(__file__)), '..')
BRANCH      = options.branch
REMOTE      = options.remote
DATE_FORMAT = "%Y-%m-%d"
DATE_STR    = datetime.now().strftime("%s" % (DATE_FORMAT))
COMMIT_TITLE_MSG    = f"OTHER: Data for {DATE_STR}"
COMMIT_BODY_MSG     = f"Collected data samples for {DATE_STR}"
FILE_NAME   = f"COVID19_PL_{DATE_STR}.json"
FILE_PATH   = os.path.join(BASE_DIR, "covid19pl/data", FILE_NAME)

# Prepare commands to execute -------------------------------------------------
COMMANDS = (
            f"git fetch {REMOTE} {BRANCH}",
            f"git rebase {REMOTE} {BRANCH}",
            f"git add {FILE_PATH}",
            f"git commit -m \"{COMMIT_TITLE_MSG}\" -m \"{COMMIT_BODY_MSG}\"",
            #f"git push {REMOTE} {BRANCH}",
           )

# Execute commands and delivery data ------------------------------------------

if not os.path.isfile(FILE_PATH):
    print(f"ERROR: File {FILE_PATH} does not exist.")
    sys.exit(1)

for cmd in COMMANDS:
    cp = subprocess.run(cmd, check=True, shell=True)

