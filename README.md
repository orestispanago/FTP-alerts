# FTP-alerts

A script to monitor FTP files uploaded by dataloggers, all-sky cameras and the thermal camera.

Gets last file stats from last subfolder ```/cams/All-sky```, ```/cams/Thermal``` and ```/dataloggers```.

Sends:

* an alert if last file was not modified within the past day

* a report if everything is OK

* an alert if FTP server offline

### Setup

```
pip install -r requirements.txt
cp .env.example .env
chmod 600 .env
```

Set the real values in `.env` (FTP and email credentials), replacing the placeholders. It is in `.gitignore`. 

Folders to check and email recipients are in `config.json`.

### Cron job

To run every day at 09:00 UTC use:

```
0 9 * * * python3 ~/FTP-alerts/main.py
```