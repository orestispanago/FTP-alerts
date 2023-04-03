import datetime
import logging
import os
import traceback
from email.utils import format_datetime
from logging import config

from config import CAMS, DATALOGGERS
from ftp_file_stats import get_last_files_stats
from mailer import send_mail

dname = os.path.dirname(__file__)
os.chdir(dname)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def alert(stat):
    subject = f"ALERT for {stat['subfolder']}"
    accessed_fmt = stat["accessed"].strftime("%Y-%m-%d %H:%M:%S%z")
    body = (
        f"FTP directory: {stat['directory']}\n"
        f"Last file: {stat['last_file']}\n"
        f"Modified: {stat['modified']}\n"
        f"Accessed: {accessed_fmt}"
    )
    send_mail(subject=subject, body=body)


def report_ok(ftp_dir):
    subject = f"REPORT OK for {ftp_dir['BASE_DIR']}"
    send_mail(subject=subject)


def check_ftp_dir(ftp_dir):
    logger.info(f"{'-' * 10} Checking: {ftp_dir['BASE_DIR']} {'-' * 10}")
    files_stats = get_last_files_stats(ftp_dir)
    too_old = []
    for stat in files_stats:
        if stat["accessed"] - stat["modified"] > datetime.timedelta(days=1):
            too_old.append(stat)
            alert(stat)
    if len(too_old) == 0:
        report_ok(ftp_dir)


def main():
    try:
        check_ftp_dir(DATALOGGERS)
        check_ftp_dir(CAMS)
    except TimeoutError as e:
        send_mail(subject="NAS OFFLINE")
        logger.warning(f"FTP server TimeoutError: \n{e}")


if __name__ == "__main__":
    try:
        main()
        logger.info(f"{'-' * 15} SUCCESS {'-' * 15}")
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
