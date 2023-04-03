# FTP-alerts

A script to monitor FTP files uploaded by dataloggers and all-sky cameras.

Gets last file stats from last subfolder ```/cams/All-sky``` and ```/dataloggers```.

Sends:

* an alert if last file was not modified within the past day

* a report if everything is OK

* an alert if FTP server offline

### Cron job

To run every day at 09:00 UTC use:

```
0 9 * * * python3 ~/FTP-alerts/main.py
```