import json
import os

dirname = os.path.dirname(__file__)
config_file = os.path.join(dirname, "config.json")

with open(config_file, "r") as f:
    configs = json.load(f)


FTP_IP = configs.get("FTP_IP")
FTP_USER = configs.get("FTP_USER")
FTP_PASS = configs.get("FTP_PASS")
DATALOGGERS = configs.get("DATALOGGERS")
CAMS = configs.get("CAMS")
EMAIL_USER = configs.get("EMAIL_USER")
EMAIL_PASS = configs.get("EMAIL_PASS")
EMAIL_RECIPIENTS = configs.get("EMAIL_RECIPIENTS")
