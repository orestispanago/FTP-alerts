import json
import os

from dotenv import load_dotenv

dirname = os.path.dirname(__file__)
config_file = os.path.join(dirname, "config.json")
load_dotenv(os.path.join(dirname, ".env"))

with open(config_file, "r") as f:
    configs = json.load(f)


FTP_IP = os.getenv("FTP_IP")
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")
DATALOGGERS = configs.get("DATALOGGERS")
CAMS = configs.get("CAMS")
THERMAL_CAMS = configs.get("THERMAL_CAMS")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECIPIENTS = configs.get("EMAIL_RECIPIENTS")
