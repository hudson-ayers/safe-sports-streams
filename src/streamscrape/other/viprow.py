"""Code for scraping from viprow."""
import logging
import re
import time

import requests
from bs4 import BeautifulSoup

from streamscrape.utils import get_ip_address

logger = logging.getLogger(__name__)

HOME = "https://www.viprow.net"

LINK = re.compile(r"Link \d+")


def scrape():
    """Scrape viprow.

    :return: A list of {"timestamp": _, "url": _, "ip": _}
    """
    all_urls = []
    page = requests.get(HOME + "/sports-live-now")
    soup = BeautifulSoup(page.text, "html.parser")

    # Search through "Open Video" links
    for video_link in soup.find_all("button", text=LINK):
        try:
            url = video_link.attrs["data-uri"]
        except KeyError:
            continue

        if url.startswith("/"):
            url = HOME + url

        event_data = {
            "timestamp": int(time.time()),
            "url": url,
            "ip": get_ip_address(url),
        }
        logger.debug("URL: {}".format(event_data))
        all_urls.append(event_data)
    return all_urls
