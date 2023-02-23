#!/usr/bin/env python3

import time
import sys
import getopt
import pychromecast
import os
import random
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def getAdhanFile(fajr):
    dirName = os.getenv("HOME") + "/adhan"
    adhanFiles = [f for f in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, f))]
    if fajr:
        adhanFiles = [x for x in adhanFiles if "_fajr" in x]
    else:
        adhanFiles = [x for x in adhanFiles if "_fajr" not in x]
    print("adhanFiles: ", adhanFiles)
    return adhanFiles[random.randrange(0,len(adhanFiles))]

def castAdhan(fileType, fajr, chromecasts):
    cast = chromecasts[0]
    cast.wait()
    #print(cast.device)
    mc = cast.media_controller

    if fileType == "adhan":
        fileAddr = f"http://{get_ip()}:8000/adhan/" + getAdhanFile(fajr)
    else:
        fileAddr = f"http://{get_ip()}:8000/adhanDua/adhanDua.mp3"
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
                print("Playing ", fileAddr)
                if fileType == "adhan":
                    while cast.media_controller.status.player_state == "PLAYING":
                        time.sleep(10)
                    castAdhan("dua", False, chromecasts)
                break
            if cast.socket_client.is_connected and has_played and player_state != "PLAYING":
                has_played = False  
                cast.media_controller.play_media(fileAddr, "audio/mp3")
            time.sleep(0.1)
            t = t - 0.1
        except KeyboardInterrupt:
            break

    

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "-fc:", ["fajr"])
    except getopt.GetoptError:
        print("python3 castAdhan.py [-f/ajr]")
        sys.exit()
    fajr = False
    for opt, arg in opts:
        if opt == "-f":
            print("Cast Adhan for Fajr")
            fajr = True
        elif opt == "-c":
            chromecast_name = arg
    
    services, browser = pychromecast.discovery.discover_chromecasts()
    print(services, browser)
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[chromecast_name])
    if not chromecasts:
        print(f'No chromecast with name "{chromecast_name}" discovered')
        sys.exit(1)
    castAdhan(fileType="adhan", fajr=fajr, chromecasts=chromecasts)
    # Shut down discovery
    browser.stop_discovery()

if __name__ == "__main__":
    main(sys.argv[1:])
