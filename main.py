import requests
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")


def scrape(url):
    """Scrape he page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    username = "tt.test.159753159753@gmail.com"
    password = os.getenv("PASSWORD")
    receiver = "tt.test.159753159753@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email was sent")


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, date, city = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND date=? AND city=?", (band, date, city))
    rows = cursor.fetchall()
    print(rows)
    return rows

if __name__ == '__main__':
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="Hey, new event was found")
        time.sleep(2)
