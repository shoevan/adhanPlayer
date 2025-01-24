import os
from requests import get

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "accept": "application/json"
}


def urlRequest(url):
    resp = get(url=url, headers=headers)
    return resp.json()


def main():
    publicIP = urlRequest("https://api.ipify.org?format=json")["ip"]
    location = urlRequest(f"http://ip-api.com/json/{publicIP}")
    lat = location["lat"]
    lon = location["lon"]
    prayerTimeCalcMethod = 3
    prayerTimeSchool = 0
    prayerTimes = urlRequest(
        f"http://api.aladhan.com/v1/timings/:date_or_timestamp?latitude={lat}&longitude={lon}&method={prayerTimeCalcMethod}&school={prayerTimeSchool}")["data"]["timings"]
    print(prayerTimes)
    with open(f"{os.environ['HOME']}/prayerTimes.txt", "w") as prayers:
        prayers.write(f"{prayerTimes['Fajr']}\n")
        prayers.write(f"{prayerTimes['Dhuhr']}\n")
        prayers.write(f"{prayerTimes['Asr']}\n")
        prayers.write(f"{prayerTimes['Maghrib']}\n")
        prayers.write(f"{prayerTimes['Isha']}\n")


if __name__ == "__main__":
    main()
