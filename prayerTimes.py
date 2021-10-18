import json
import urllib.request
import os

def urlRequest(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = response.read()
    return json.loads(data)

def main():
    publicIP = urlRequest("https://api.ipify.org?format=json")["ip"]
    location = urlRequest(f"http://ip-api.com/json/{publicIP}")
    lat = location["lat"]
    lon = location["lon"]
    prayerTimeCalcMethod = 3
    prayerTimeSchool =1
    prayerTimes = urlRequest(f"http://api.aladhan.com/v1/timings/:date_or_timestamp?latitude={lat}&longitude={lon}&method={prayerTimeCalcMethod}&school={prayerTimeSchool}")["data"]["timings"]
    with open(f"{os.environ['HOME']}/prayerTimes.txt", "w") as prayers:
        prayers.write(f"{prayerTimes['Fajr']}\n")
        prayers.write(f"{prayerTimes['Dhuhr']}\n")
        prayers.write(f"{prayerTimes['Asr']}\n")
        prayers.write(f"{prayerTimes['Maghrib']}\n")
        prayers.write(f"{prayerTimes['Isha']}\n")

if __name__ == "__main__":
    main()
