## check if ISS is near

import requests
from datetime import datetime as dt
from dateutil.parser import isoparse
import time as t
import smtplib

MY_EMAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"
MY_SMTP = "YOUR SMTP"
MY_LAT = 51.44083 # YOUR LAT
MY_LONG = 5.47778 # YOUR LAT


def utc_to_local(utc_datetime):
    now_time = t.time()
    offset = dt.fromtimestamp(now_time) - dt.utcfromtimestamp(now_time)
    return utc_datetime + offset


def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = isoparse(data["results"]["sunrise"])
    sunrise = utc_to_local(sunrise).hour
    sunset = isoparse(data["results"]["sunset"])
    sunset = utc_to_local(sunset).hour
    time_now = dt.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    t.sleep(60)
    if iss_overhead() and is_night():
        with smtplib.SMTP(MY_SMTP, 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject: Look Up\n\nThe ISS is above and near you.".encode("utf8")
            )