"""Code for scraping from RojaDirecta."""
import logging
import time

import requests
from bs4 import BeautifulSoup

from streamscrape.utils import get_ip_address

logger = logging.getLogger(__name__)

HOME = "http://www.rojadirecta.me"


def scrape():
    """Scrape RojaDirecta.

    :return: A list of {"timestamp": _, "url": _, "ip": _}
    """
    all_urls = []
    page = requests.get(HOME)
    soup = BeautifulSoup(page.text, "html.parser")
    url_table = soup.find("div", id="agendadiv")
    for a in url_table.find_all("a"):
        try:
            href = a.attrs["href"]
        except KeyError:
            continue

        # skip p2p acestream urls
        if any(s in href for s in ["rojadirecta.me", "elgoles.me", "arenavision.link"]):
            continue

        # Go to the actual URL if rojadirecta wants to redirect
        if href.startswith("http://it.rojadirecta.eu/goto/http"):
            href = href.replace("http://it.rojadirecta.eu/goto/", "")
        elif href.startswith("http://it.rojadirecta.eu/goto/"):
            href = href.replace("it.rojadirecta.eu/goto/", "")

        event_data = {
            "timestamp": int(time.time()),
            "url": href,
            "ip": get_ip_address(href),
        }
        logger.debug("RojaDirecta URL data: {}".format(event_data))
        all_urls.append(event_data)

    return all_urls
