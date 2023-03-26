import datetime
import logging
import os
import traceback
from email.utils import format_datetime
from ftplib import FTP
from logging import config

import pandas as pd

from config import DATALOGGERS, FTP_BASE_DIR, FTP_IP, FTP_PASS, FTP_USER
from mailer import send_mail

dname = os.path.dirname(__file__)
os.chdir(dname)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def get_last_modified_file(ftp, remote_dir):
    ftp.cwd(remote_dir)
    entries = [i for i in ftp.mlsd()]
    last_entry = entries[-1]
    fname = last_entry[0]
    modify = last_entry[1]["modify"]
    modified = datetime.datetime.strptime(modify, "%Y%m%d%H%M%S")
    modified = modified.replace(tzinfo=datetime.timezone.utc)
    return fname, modified


def get_dataloggers_status(ftp_folders, utc_now):
    dataloggers_status = []
    with FTP(FTP_IP, FTP_USER, FTP_PASS) as ftp:
        for datalogger in DATALOGGERS:
            remote_dir = f"{FTP_BASE_DIR}/{datalogger}/{utc_now.year}"
            fname, modified = get_last_modified_file(ftp, remote_dir)
            status = {
                "name": datalogger,
                "last_file": fname,
                "last_modified": modified,
            }
            dataloggers_status.append(status)
    return dataloggers_status


def alert(df, utc_now):
    df_alert = df.loc[
        (utc_now - df["last_modified"]) > datetime.timedelta(days=1)
    ]
    if len(df_alert) > 0:
        for index, row in df_alert.iterrows():
            subject = f"ALERT for {row['name']} datalogger"
            body = f"Alert generated at {format_datetime(utc_now)}"
            send_mail(df_alert.to_html(index=False), subject=subject, body=body)
    else:
        subject = "REPORT for LapUp dataloggers"
        body = f"Everyting OK! Report generated at {format_datetime(utc_now)}"
        send_mail(df.to_html(index=False), subject=subject, body=body)
    logger.info(f"{'-' * 15} SUCCESS {'-' * 15}")


def main():
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    dataloggers_status = get_dataloggers_status(DATALOGGERS, utc_now)
    df = pd.DataFrame(dataloggers_status)
    alert(df, utc_now)


if __name__ == "__main__":
    try:
        main()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
