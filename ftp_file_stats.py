import datetime
from ftplib import FTP

from config import DATALOGGERS, FTP_BASE_DIR, FTP_IP, FTP_PASS, FTP_USER


def modified_str_to_utc(modified_str):
    modified_dt = datetime.datetime.strptime(modified_str, "%Y%m%d%H%M%S")
    modified_utc = modified_dt.replace(tzinfo=datetime.timezone.utc)
    return modified_utc


def get_last_file_stats(ftp, remote_dir):
    """Enters last FTP directory recursively and gets last file stats"""
    ftp.cwd(remote_dir)
    folders, files = [], []
    for entry in ftp.mlsd():
        if entry[1]["type"] == "dir":
            folders.append(entry)
        elif entry[1]["type"] == "file":
            files.append(entry)
    folders = sorted(folders)
    if len(folders) > 0:
        last_folder = folders[-1]
        remote_dir = f"{remote_dir}/{last_folder[0]}"
        return get_last_file_stats(ftp, remote_dir)
    files = sorted(files)
    last_file = files[-1]
    fname = last_file[0]
    modified = last_file[1]["modify"]
    return remote_dir, fname, modified


def get_last_files_stats(base_dir=FTP_BASE_DIR, subfolders=DATALOGGERS):
    dataloggers_stats = []
    for subfolder in subfolders:
        remote_folder = f"{base_dir}/{subfolder}"
        with FTP(FTP_IP, FTP_USER, FTP_PASS) as ftp:
            remote_folder = f"{base_dir}/{subfolder}"
            dirname, fname, modified = get_last_file_stats(ftp, remote_folder)
        modified_utc = modified_str_to_utc(modified)
        stats = {
            "name": subfolder,
            "directory": dirname,
            "last_file": fname,
            "modified": modified_utc,
        }
        dataloggers_stats.append(stats)
    return dataloggers_stats
