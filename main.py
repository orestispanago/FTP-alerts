import datetime
import logging
import os
import traceback
from logging import config

from config import CAMS, DATALOGGERS, FTP_IP, THERMAL_CAMS
from ftp_file_stats import get_last_files_stats
from mailer import send_mail

dname = os.path.dirname(__file__)
os.chdir(dname)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def alert(stat):
    subject = f"FTP check: ALERT for {stat['subfolder']}"
    accessed_fmt = stat["accessed"].strftime("%Y-%m-%d %H:%M:%S%z")
    body = (
        f"FTP directory: {stat['directory']}\n"
        f"Last file: {stat['last_file']}\n"
        f"Modified: {stat['modified']}\n"
        f"Accessed: {accessed_fmt}"
    )
    send_mail(subject=subject, body=body)


def report_ok():
    lines = ["Checked subfolders:"]
    for ftp_dir in (DATALOGGERS, CAMS, THERMAL_CAMS):
        lines.append(
            f"{ftp_dir['BASE_DIR']}: {', '.join(ftp_dir['SUBFOLDERS'])}"
        )
    send_mail(subject="FTP check: OK", body="\n".join(lines))


def is_too_old(stat):
    too_old = True
    if stat["modified"] is not None:
        if stat["accessed"] - stat["modified"] <= datetime.timedelta(days=1):
            too_old = False
    return too_old


def check_ftp_dir(ftp_dir):
    logger.info(f"{'-' * 10} Checking: {ftp_dir['BASE_DIR']} {'-' * 10}")
    files_stats = get_last_files_stats(ftp_dir)
    too_old = []
    for stat in files_stats:
        if is_too_old(stat):
            too_old.append(stat)
            alert(stat)
    return too_old


def main():
    try:
        too_old = check_ftp_dir(DATALOGGERS)
        too_old += check_ftp_dir(CAMS)
        too_old += check_ftp_dir(THERMAL_CAMS)
        if len(too_old) == 0:
            report_ok()
    except OSError as e:
        # Timeout, no route to host, connection refused: the NAS is not reachable
        logger.warning(f"FTP server unreachable: \n{e}")
        send_mail(subject=f"NAS OFFLINE: {FTP_IP}")


def report_failure(error_trace):
    logger.error("uncaught exception: %s", error_trace)
    try:
        send_mail(subject="DAILY CHECK FAILED")
    except Exception:
        logger.error("could not send failure mail: %s", traceback.format_exc())


if __name__ == "__main__":
    try:
        main()
        logger.info(f"{'-' * 15} SUCCESS {'-' * 15}")
    except:
        report_failure(traceback.format_exc())
