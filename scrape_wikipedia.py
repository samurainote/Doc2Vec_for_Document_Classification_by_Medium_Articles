import csv
import requests
from bs4 import BeautifulSoup

def scrape_data(url):

    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find_all("table")[1]

    rows = table.select("tbody > tr")

    header = [th.text.rstrip() for th in rows[0].find_all("th")]

    with open("gdp.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for row in rows[1:]:
            data = [th.text.rstrip() for th in rows[0].find_all("td")]
            writer.writerow(data)

if __name__=="main":
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    scrape_data(url)
