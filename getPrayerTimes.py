


def getPrayerTimes():
    print("Executing prayer time script for today at ", datetime.now())
    with open("prayerTimes.txt", "r") as prayerTimes:
        for lines in prayerTimes:
            print("Scheduling adhan for ", lines)
            schedule.every().day.at(lines.strip().replace("\"","")).do(setPrayerTimes)

