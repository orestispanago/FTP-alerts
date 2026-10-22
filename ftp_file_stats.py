import datetime
from ftplib import FTP

from config import FTP_IP, FTP_PASS, FTP_USER


def modified_str_to_utc(modified_str):
    modified_dt = datetime.datetime.strptime(modified_str, "%Y%m%d%H%M%S")
    modified_utc = modified_dt.replace(tzinfo=datetime.timezone.utc)
    return modified_utc


def list_folders_and_files(ftp, remote_dir):
    ftp.cwd(remote_dir)
    folders, files = [], []
    for entry in ftp.mlsd():
        if entry[1]["type"] == "dir":
            folders.append(entry)
        elif entry[1]["type"] == "file":
            files.append(entry)
    return sorted(folders), sorted(files)


def get_last_file_stats(ftp, remote_dir):
    """Searches folders newest first, skipping empty ones. Returns None if no file is found"""
    folders, files = list_folders_and_files(ftp, remote_dir)
    last_file_stats = None
    index = len(folders) - 1
    while last_file_stats is None and index >= 0:
        folder_path = f"{remote_dir}/{folders[index][0]}"
        last_file_stats = get_last_file_stats(ftp, folder_path)
        index -= 1
    if last_file_stats is None and len(files) > 0:
        last_file = files[-1]
        last_file_stats = (remote_dir, last_file[0], last_file[1]["modify"])
    return last_file_stats


def make_stats(subfolder, remote_folder, last_file_stats):
    accessed_utc = datetime.datetime.now(datetime.timezone.utc)
    if last_file_stats is None:
        dirname = remote_folder
        fname = "no files found"
        modified_utc = None
    else:
        dirname, fname, modified = last_file_stats
        modified_utc = modified_str_to_utc(modified)
    stats = {
        "subfolder": subfolder,
        "directory": dirname,
        "last_file": fname,
        "modified": modified_utc,
        "accessed": accessed_utc,
    }
    return stats


def get_last_files_stats(ftp_dir):
    base_dir = ftp_dir.get("BASE_DIR")
    dataloggers_stats = []
    with FTP(FTP_IP, FTP_USER, FTP_PASS, timeout=30) as ftp:
        for subfolder in ftp_dir.get("SUBFOLDERS"):
            remote_folder = f"{base_dir}/{subfolder}"
            last_file_stats = get_last_file_stats(ftp, remote_folder)
            stats = make_stats(subfolder, remote_folder, last_file_stats)
            dataloggers_stats.append(stats)
    return dataloggers_stats
