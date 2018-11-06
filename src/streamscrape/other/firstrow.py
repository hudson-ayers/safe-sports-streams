"""Code for scraping from firstrowonly.eu."""
import logging
import re
import time

import requests
from bs4 import BeautifulSoup

from streamscrape.utils import get_ip_address

logger = logging.getLogger(__name__)
HOME = "http://firstrowonly.eu"

STREAMS = re.compile(r"(Link \d+|HD \w+)")


def scrape():
    """Scrape firstrowonly.

    :return: A list of {"timestamp": _, "url": _, "ip": _}
    """
    category_urls = [
        HOME,  # soccer is default
        "http://firstrowonly.eu/sport/american-football.html",
        "http://firstrowonly.eu/sport/basketball.html",
        "http://firstrowonly.eu/sport/rugby.html",
        "http://firstrowonly.eu/sport/rugby.html",
        "http://firstrowonly.eu/sport/ice-hockey.html",
        "http://firstrowonly.eu/sport/olympics.html",
        "http://firstrowonly.eu/sport/boxing-wwe-ufc.html",
        "http://firstrowonly.eu/sport/tennis.html",
        "http://firstrowonly.eu/sport/baseball.html",
        "http://firstrowonly.eu/sport/motosport.html",
        "http://firstrowonly.eu/sport/golf.html",
        "http://firstrowonly.eu/sport/darts.html",
        "http://firstrowonly.eu/sport/snooker.html",
        "http://firstrowonly.eu/sport/aussie-rules.html",
        "http://firstrowonly.eu/sport/handball.html",
        "http://firstrowonly.eu/sport/cricket.html",
        "http://firstrowonly.eu/sport/others.html",
        "http://firstrowonly.eu/sport/tv-box.html",
    ]
    all_urls = []
    unique_urls = set()
    for category_url in category_urls:
        page = requests.get(category_url)
        soup = BeautifulSoup(page.text, "html.parser")
        # Grab all the stream links
        for stream_link in soup(text=STREAMS):
            try:
                url = stream_link.parent.attrs["href"]
            except KeyError:
                continue

            if url.startswith("/watch"):
                url = HOME + url

            if url in unique_urls:
                continue
            else:
                unique_urls.add(url)
                event_data = {
                    "timestamp": int(time.time()),
                    "url": url,
                    "ip": get_ip_address(url),
                }
                all_urls.append(event_data)
    return all_urls
