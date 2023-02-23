#!/usr/bin/env python3

import sys
import os
import getopt
from crontab import CronTab, CronSlices

def setCron(chromecast_name):
    cron = CronTab(user="pi")
    cron.remove_all()
    prayerTimeFetch = cron.new(command=f"python3 {os.getenv('HOME')}/adhanPlayer/prayerTimes.py >> {os.getenv('HOME')}/prayerCron.txt", comment="prayerTimeFetch")
    prayerTimeFetch.setall("0 0 * * *")
    setPrayerTime = cron.new(command=f"python3 {os.getenv('HOME')}/adhanPlayer/prayerCron.py >> {os.getenv('HOME')}/prayerCron.txt", comment="setPrayerTime")
    setPrayerTime.setall("5 0 * * *")
    prayerNames = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    x = 0
    with open(os.getenv("HOME") + "/prayerTimes.txt", "r") as prayerTimes:
        for lines in prayerTimes:
            if x == 0:
                fajrSwitch = "-f"
            else:
                fajrSwitch = ""
            lines = lines.strip().replace("\"","")
            print("Scheduling adhan for", lines)


            timeSlot = lines[3:5] + " " + lines[0:2] + " * * *" 
#            print("Time slot valid: ", timeSlot, CronSlices.is_valid(timeSlot))
            prayer = cron.new(f"python3 {os.getenv('HOME')}/adhanPlayer/castAdhan.py {fajrSwitch} -c \"{chromecast_name}\" >> {os.getenv('HOME')}/prayerCron.txt", comment=prayerNames[x])
            prayer.setall(timeSlot)
            x += 1
    cron.write()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "c:")
    except getopt.GetoptError:
        print("python3 castAdhan.py [-f/ajr]")
        sys.exit()
    for opt, arg in opts:
        if opt == "-c":
            chromecast_name = arg
    setCron(chromecast_name=chromecast_name)

if __name__ == "__main__":
    main(sys.argv[1:])
