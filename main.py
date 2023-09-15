import icalendar
import calendar
import json
import datetime
import pytz


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


with open("schedule.json") as f:
    schedule = json.load(f)

calendar = icalendar.Calendar()
calendar.add("prodid", "STANKIN")
calendar.add("version", "2.0")

for pair in schedule:
    classroom = pair["classroom"]
    lecturer = pair["lecturer"]
    title = pair["title"]
    ptype = pair["type"][0].lower()
    time_start = [int(t) for t in pair["time"]["start"].split(":")]
    time_end = [int(t) for t in pair["time"]["end"].split(":")]
    for date in pair["dates"]:
        if date["frequency"] == "every":
            start_date = [int(d) for d in date["date"].split("-")[:3]]
            end_date = [int(d) for d in date["date"].split("-")[3:]]
            start_date = datetime.date(start_date[0], start_date[1], start_date[2])
            end_date = datetime.date(end_date[0], end_date[1], end_date[2])
            weekday = start_date.weekday()
            for day in daterange(start_date, end_date):
                if day.weekday() == weekday:
                    iPair = icalendar.Event()
                    iPair.add(
                        "summary",
                        "{} {}, пр. {}".format(
                            "Лекция" if ptype == "l" else "Семинар",
                            title.lower(),
                            lecturer if lecturer != "" else "не указан",
                        ),
                    )
                    iPair.add(
                        "dtstart",
                        datetime.datetime(
                            day.year,
                            day.month,
                            day.day,
                            time_start[0],
                            time_start[1],
                            tzinfo=pytz.timezone("Europe/Moscow"),
                        ),
                    )
                    iPair.add(
                        "dtend",
                        datetime.datetime(
                            day.year,
                            day.month,
                            day.day,
                            time_end[0],
                            time_end[1],
                            tzinfo=pytz.timezone("Europe/Moscow"),
                        ),
                    )
                    iPair.add("dtstamp", datetime.datetime.now())
                    iPair["location"] = icalendar.vText(classroom)
                    calendar.add_component(iPair)
        if date["frequency"] == "once":
            date = [int(d) for d in date["date"].split("-")]
            date = datetime.date(date[0], date[1], date[2])
            weekday = date.weekday()
            iPair = icalendar.Event()
            iPair.add(
                "summary",
                "{} {}, пр. {}".format(
                    "Лекция" if ptype == "l" else "Семинар",
                    title.lower(),
                    lecturer if lecturer != "" else "не указан",
                ),
            )
            iPair.add(
                "dtstart",
                datetime.datetime(
                    date.year,
                    date.month,
                    date.day,
                    time_start[0],
                    time_start[1],
                    tzinfo=pytz.timezone("Europe/Moscow"),
                ),
            )
            iPair.add(
                "dtend",
                datetime.datetime(
                    date.year,
                    date.month,
                    date.day,
                    time_end[0],
                    time_end[1],
                    tzinfo=pytz.timezone("Europe/Moscow"),
                ),
            )
            iPair.add("dtstamp", datetime.datetime.now())
            calendar.add_component(iPair)


with open("schedule.ics", "wb") as f:
    f.write(calendar.to_ical())
