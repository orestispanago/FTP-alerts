import datetime
from ftplib import FTP

from config import FTP_IP, FTP_PASS, FTP_USER


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


def get_last_files_stats(ftp_dir):
    base_dir = ftp_dir.get("BASE_DIR")
    dataloggers_stats = []
    with FTP(FTP_IP, FTP_USER, FTP_PASS) as ftp:
        for subfolder in ftp_dir.get("SUBFOLDERS"):
            remote_folder = f"{base_dir}/{subfolder}"
            dirname, fname, modified = get_last_file_stats(ftp, remote_folder)
            modified_utc = modified_str_to_utc(modified)
            accessed_utc = datetime.datetime.now(datetime.timezone.utc)
            stats = {
                "subfolder": subfolder,
                "directory": dirname,
                "last_file": fname,
                "modified": modified_utc,
                "accessed": accessed_utc,
            }
            dataloggers_stats.append(stats)
    return dataloggers_stats
