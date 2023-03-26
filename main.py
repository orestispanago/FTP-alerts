import datetime
from email.utils import format_datetime
from ftplib import FTP

FTP_IP = ""
FTP_USER = ""
FTP_PASS = ""
FTP_DIR = "/dataloggers"


def get_last_file(ftp, remote_dir):
    ftp.cwd(remote_dir)
    entries = [i for i in ftp.mlsd()]
    last_entry = entries[-1]
    fname = last_entry[0]
    modify = last_entry[1]["modify"]
    modified = datetime.datetime.strptime(modify, "%Y%m%d%H%M%S")
    modified = modified.replace(tzinfo=datetime.timezone.utc)
    return fname, modified


def get_offline_dataloggers(ftp_folders):
    offline_dataloggers = []
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    with FTP(FTP_IP, FTP_USER, FTP_PASS) as ftp:
        for folder in ftp_folders:
            remote_dir = f"{FTP_DIR}/{folder}/{utc_now.year}"
            fname, modified = get_last_file(ftp, remote_dir)
            datalogger = {
                "name": folder,
                "last_file": fname,
                "last_upload": modified,
            }
            if utc_now - modified > datetime.timedelta(minutes=2):
                offline_dataloggers.append(datalogger)
    return offline_dataloggers


folders = ["meteo", "solar", "nilu", "rsi", "koukouli"]

offline = get_offline_dataloggers(folders)

if len(offline) == 0:
    print("Everything OK!")
else:
    for datalogger in offline:
        print("======================= ALERT =======================")
        print(f"Alert for datalogger: {datalogger['name']}")
        print(f"Last file: {datalogger['last_file']}")
        print(f"Last uploaded at: {datalogger['last_upload']}")
