"""Code for scraping from stream2watch.org."""
import logging
import time

import requests
from bs4 import BeautifulSoup

from streamscrape.utils import get_ip_address

logger = logging.getLogger(__name__)

HOME = "https://www.stream2watch.org"


def scrape():
    """Scrape stream2watch.

    :return: A list of {"timestamp": _, "url": _, "ip": _}
    """
    all_urls = []
    page = requests.get(HOME)
    soup = BeautifulSoup(page.text, "html.parser")
    url_table = soup.find("div", class_="list_streams")
    for a in url_table.find_all("a", class_="title-t-a"):
        try:
            href = a.attrs["href"]
        except KeyError:
            continue
        event_data = {
            "timestamp": int(time.time()),
            "url": href,
            "ip": get_ip_address(href),
        }
        logger.debug("stream2watch URL data: {}".format(event_data))
        all_urls.append(event_data)

    return all_urls
