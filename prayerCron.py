#!/usr/bin/env python3

import sys
import os
from crontab import CronTab, CronSlices

def setCron():
    cron = CronTab(user="pi")
    cron.remove_all()
    prayerTimeFetch = cron.new(command=os.getenv('HOME') + "/alarm/prayerTimes.py >> " + os.getenv('HOME') + "/prayerCron.txt", comment="prayerTimeFetch")
    prayerTimeFetch.setall("0 0 * * *")
    setPrayerTime = cron.new(command="python3 " + os.getenv("HOME") + "/alarm/prayerCron.py >> " + os.getenv("HOME") + "/prayerCron.txt", comment="setPrayerTime")
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
            prayer = cron.new("python3 " + os.getenv("HOME") + "/alarm/castAdhan.py " + fajrSwitch + " >> " + os.getenv("HOME") + "/prayerCron.txt", comment=prayerNames[x])
            prayer.setall(timeSlot)
            x += 1
    cron.write()

def main():

    setCron()

if __name__ == "__main__":
    main()
