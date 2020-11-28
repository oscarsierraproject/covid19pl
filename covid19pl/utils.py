#!/usr/bin/env python3
# -*- coding: 'utf-8' -*-

__author__      = "oscarsierraproject.eu"
__copyright__   = "Copyright 2020, oscarsierraproject.eu"
__license__     = "GNU General Public License 3.0"
__date__        = "28th November 2020"
__maintainer__  = "oscarsierraproject.eu"
__email__       = "oscarsierraproject@protonmail.com"
__status__      = "Development"

from dotenv import load_dotenv
import email.message
from email.mime.text import MIMEText
import logging
import logging.config
import os
import pandas as pd
import smtplib
from typing import Dict

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


def display_todays_stats_for_all_locations (
        gathered_data:Dict[str, pd.DataFrame]) -> None:
    """ Display actual summary data and 1 day change. """
    print(  "%-20s: %7s %7s %8s %7s %7s" % \
            ("Location", "Total", "Death", "CHANGE:", "Total", "Death"))
    for loc, data in gathered_data.items():
        infected_total = data["total"].sum()
        infected_today = data["total"].iat[-1]
        dead_total = data["dead"].sum()
        dead_today = data["dead"].iat[-1]
        print(  "%-20s: %7s %7s %8s %7s %7s" % \
                (loc, infected_total, dead_total,
                 "", infected_today, dead_today))


def get_todays_stats_for_location_as_str(
        location:str, data:pd.DataFrame) -> str:
    """ Convert current summary data into string """
    date = str(data["date"].iat[-1])
    infected_total = data["total"].sum()
    infected_today = data["total"].iat[-1]
    dead_total = data["dead"].sum()
    dead_today = data["dead"].iat[-1]
    return f"{location} on {date} has {infected_total} infections in total"\
           f"with {infected_today} new infections and {dead_today} new deaths."


def send_summary_email(recipient, data):
    """ Send email with summary data """
    SRV_ADDR    = os.getenv("EMAIL_SMTP_SRV_ADDR")
    SRV_PORT    = os.getenv("EMAIL_SMTP_SRV_PORT")
    SRV_LOGIN   = os.getenv("EMAIL_SMTP_SRV_LOGIN")
    SRV_PWD     = os.getenv("EMAIL_SMTP_SRV_PASSWORD")

    if None in [SRV_ADDR, SRV_PORT, SRV_LOGIN, SRV_PWD]:
        msg = "Unable to send email, no SMTP server configuration provided"
        self.logger.error(msg)
        return
    TEXT = ["Summary of COVID19 cases in Poland.", ""]
    for loc, data in data.items():
        TEXT.append(get_todays_stats_for_location_as_str(loc, data))
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

