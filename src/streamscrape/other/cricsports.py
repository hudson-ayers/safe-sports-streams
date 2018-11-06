"""Code for scraping from cricsports.sc."""
import logging
import multiprocessing as mp
import re
import time

import requests
from bs4 import BeautifulSoup

from streamscrape.utils import get_ip_address

logger = logging.getLogger(__name__)

HOME = "http://cricsports.sc"

# Only want to compile this once to reduce overhead
WATCH = re.compile(r"Watch")


def _scrape_event(url):
    """Scrape the stream URLs from the event URL.

    :param url: The event URL to scrape for stream links.
    :type url: string
    :return: A tuple of dict {"timestamp": _, "url": _, "ip": _}
    """
    urls = set()
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    # Grab all the watch button links
    for watch_btn in soup(text=WATCH):
        try:
            url = watch_btn.parent.attrs["href"]
        except KeyError:
            continue
        event_data = (int(time.time()), url, get_ip_address(url))
        urls.add(event_data)
        logger.debug("URL: {}".format(event_data))
    return tuple({"timestamp": e[0], "url": e[1], "ip": e[2]} for e in urls)


def scrape():
    """Scrape cricsports.

    :return: A list of {"timestamp": _, "url": _, "ip": _}
    """
    all_urls = []
    page = requests.get(HOME)
    soup = BeautifulSoup(page.text, "html.parser")
    event_urls = set(
        url_div.find("a").attrs["href"]
        for url_div in soup.find_all("div", class_="title-and-icon")
    )

    # Process all urls in parallel.
    with mp.Pool(mp.cpu_count()) as p:
        results = p.map(_scrape_event, event_urls)
        for event_urls in results:
            all_urls.extend(url for url in event_urls)

    return all_urls
