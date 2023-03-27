# FTP-alerts

A script to monitor FTP files uploaded by dataloggers and all-sky cameras.

Gets last file stats from last subfolder ```/cams/All-sky``` and ```/dataloggers```.

Sends:

* an alert if last file was not modified within the past day, or

* a report with all last files stats if everything is OK

### Cron job

To run every day at 09:00 UTC use:

```
0 9 * * * python3 ~/FTP-alerts/main.py
```