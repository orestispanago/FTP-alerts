import datetime
import logging
import os
import traceback
from email.utils import format_datetime
from logging import config

import pandas as pd

from config import CAMS, DATALOGGERS
from ftp_file_stats import get_last_files_stats
from mailer import send_mail

dname = os.path.dirname(__file__)
os.chdir(dname)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def main(ftp_dir):
    logger.info(
        f"{'-' * 10} Running main() for {ftp_dir.get('BASE_DIR')} {'-' * 10}"
    )
    stats = get_last_files_stats(ftp_dir)
    df = pd.DataFrame(stats)
    utc_now = datetime.datetime.now(datetime.timezone.utc)
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
        subject = f"REPORT for LapUp {ftp_dir.get('BASE_DIR')}"
        body = f"Everyting OK! Report generated at {format_datetime(utc_now, usegmt=True)}"
        send_mail(df.to_html(index=False), subject=subject, body=body)


if __name__ == "__main__":
    try:
        main(DATALOGGERS)
        main(CAMS)
        logger.info(f"{'-' * 15} SUCCESS {'-' * 15}")
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
