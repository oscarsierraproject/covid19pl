#!/usr/bin/env python3
# -*- coding: 'utf-8' -*-

__author__      = "oscarsierraproject.eu"
__copyright__   = "Copyright 2020, oscarsierraproject.eu"
__license__     = "GNU General Public License 3.0"
__date__        = "25th March 2020"
__maintainer__  = "oscarsierraproject.eu"
__email__       = "oscarsierraprojectk@protonmail.com"
__status__      = "Development"

from dotenv import load_dotenv
import logging
import logging.config
import os

# Load environment variables ---------------------------------------------------
def load_env_variables(env_file_path):
    if os.path.isfile(env_file_path):
        load_dotenv( dotenv_path = env_file_path)
    else:
        raise FileNotFoundError("Environment file '%s' does not exist!" %\
                                 env_file_path)
# ------------------------------------------------------------------------------

# Setup logging facility to improve execution readability ----------------------
def setup_root_logger():
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
    return root_logger
# ------------------------------------------------------------------------------
