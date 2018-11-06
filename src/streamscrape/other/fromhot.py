"""Code for scraping from FromHot."""
import logging
import time

import requests
from bs4 import BeautifulSoup

from streamscrape.utils import get_ip_address

logger = logging.getLogger(__name__)

HOME = "http://www.fromhot.com"


def scrape():
    """Scrape FromHot.

    :return: A list of {"timestamp": _, "url": _, "ip": _}
    """
    all_urls = []
    page = requests.get(HOME)
    soup = BeautifulSoup(page.text, "html.parser")

    # Search through "Open Video" links
    for video_link in soup.find_all("a", title="Open Video"):
        try:
            url = video_link.attrs["href"]
        except KeyError:
            continue
        event_data = {
            "timestamp": int(time.time()),
            "url": url,
            "ip": get_ip_address(url),
        }
        logger.debug("URL: {}".format(event_data))
        all_urls.append(event_data)
    return all_urls
