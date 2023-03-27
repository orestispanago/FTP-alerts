import json
import os

dirname = os.path.dirname(__file__)
config_file = os.path.join(dirname, "config.json")

with open(config_file, "r") as f:
    configs = json.load(f)


FTP_IP = configs.get("FTP_IP")
FTP_USER = configs.get("FTP_USER")
FTP_PASS = configs.get("FTP_PASS")
FTP_BASE_DIR = configs.get("FTP_BASE_DIR")
EMAIL_USER = configs.get("EMAIL_USER")
EMAIL_PASS = configs.get("EMAIL_PASS")
EMAIL_RECIPIENTS = configs.get("EMAIL_RECIPIENTS")
DATALOGGERS_DIR = configs.get("DATALOGGERS_DIR")
DATALOGGERS = configs.get("DATALOGGERS")
CAMS_DIR = configs.get("CAMS_DIR")
CAMS = configs.get("CAMS")
