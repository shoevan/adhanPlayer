#!/usr/bin/env python

import schedule
import subprocess
import time
import sys
import argparse
import zeroconf
import pychromecast
import os
from datetime import datetime
import http.server
import socketserver
import _thread
import random

chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Kitchen speaker"])
if not chromecasts:
    print('No chromecast with name "{}" discovered'.format("Kitchen speaker"))
    sys.exit(1)

def startHttpServer():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port ", PORT)
        httpd.serve_forever()

def getAdhanFile():
    dirName = "adhan"
    adhanFiles = [f for f in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, f))]
    return adhanFiles[random.randrange(0,len(adhanFiles))]

def castAdhan():
    cast = chromecasts[0]
    cast.wait()
    print(cast.device)
    mc = cast.media_controller
    fileAddr = "http://192.168.1.61:8000/adhan/" + getAdhanFile()
    cast.media_controller.play_media(fileAddr, "audio/mp3")

    # Wait for player_state PLAYING
    player_state = None
    t = 30
    has_played = False
    while True:
        try:
            if player_state != cast.media_controller.status.player_state:
                player_state = cast.media_controller.status.player_state
                print("Player state:", player_state)
            if player_state == "PLAYING":
                has_played = True
                print("Playing... ")
                break
            if cast.socket_client.is_connected and has_played and player_state != "PLAYING":
                has_played = False  
                cast.media_controller.play_media(fileAddr, "audio/mp3")
            time.sleep(0.1)
            t = t - 0.1
        except KeyboardInterrupt:
            break

    # Shut down discovery
    browser.stop_discovery()

def setPrayerTimes():
    print("Prayer time has been reached at ", datetime.now())
    castAdhan()
    return schedule.CancelJob

def getPrayerTimes():
    print("Executing prayer time script for today at ", datetime.now())
    with open("prayerTimes.txt", "r") as prayerTimes:
        for lines in prayerTimes:
            print("Scheduling adhan for ", lines)
            schedule.every().day.at(lines.strip().replace("\"","")).do(setPrayerTimes)

def runPrayerTimeFetch():
    subprocess.run("/home/pi/project/curl")

def main(): 
    _thread.start_new_thread(startHttpServer, ())
    schedule.every().day.at("00:00").do(runPrayerTimeFetch)
    schedule.every().day.at("00:10").do(getPrayerTimes)
    #runPrayerTimeFetch()
    getPrayerTimes() 
    #castAdhan()
    while True:
        schedule.run_pending()
        #print("Current time... ", datetime.now()," sleeping for 60s...", flush=True)
        #print("Current time... ", datetime.now()," sleeping for 60s...")
        time.sleep(60)

if __name__ == "__main__":
    main()
