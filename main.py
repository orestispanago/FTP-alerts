import datetime
import logging
import os
import traceback
from email.utils import format_datetime
from logging import config

import pandas as pd

from config import CAMS, CAMS_DIR, DATALOGGERS, DATALOGGERS_DIR
from ftp_file_stats import get_last_files_stats
from mailer import send_mail

dname = os.path.dirname(__file__)
os.chdir(dname)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def alert(df, utc_now):
    df_alert = df.loc[(utc_now - df["modified"]) > datetime.timedelta(days=1)]
    if len(df_alert) > 0:
        for index, row in df_alert.iterrows():
            subject = f"ALERT for {row['name']}"
            body = f"Alert generated at {format_datetime(utc_now, usegmt=True)}"
            df_alert = df_alert.T
            send_mail(
                df_alert.to_html(header=False), subject=subject, body=body
            )
    else:
        subject = "REPORT for LapUp FTP"
        body = f"Everyting OK! Report generated at {format_datetime(utc_now, usegmt=True)}"
        send_mail(df.to_html(index=False), subject=subject, body=body)


def main(base_dir, subfolders):
    logger.info(f"{'-' * 10} Running main() for {base_dir} {'-' * 10}")
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    stats = get_last_files_stats(base_dir=base_dir, subfolders=subfolders)
    df = pd.DataFrame(stats)
    alert(df, utc_now)


if __name__ == "__main__":
    try:
        main(DATALOGGERS_DIR, DATALOGGERS)
        main(CAMS_DIR, CAMS)
        logger.info(f"{'-' * 15} SUCCESS {'-' * 15}")
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
