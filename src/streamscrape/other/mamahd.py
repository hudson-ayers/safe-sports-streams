"""Code for scraping from mamahd."""
import logging
import multiprocessing as mp
import socket
import time

import requests
from bs4 import BeautifulSoup

from streamscrape.utils import get_ip_address

logger = logging.getLogger(__name__)

HOME = "https://www.mamahd.org"


def _scrape_event(url):
    """Scrape a specific event page for stream links.

    MAMAHD embeds just the video player from other websites on their page.
    This returns BOTH the MAMAHD page, and the embedded page.
    """
    urls = set()

    # Ignore SSL errors
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, "html.parser")

    # Grab all the watch button links
    try:
        for a in soup.find("div", id="streamtable").find_all("a"):
            try:
                if "stream-href" in a.attrs["class"]:
                    # Get BOTH the mamahd url and the embeded URL
                    url = a.attrs["href"]
                    event_data = (int(time.time()), url, get_ip_address(url))
                    urls.add(event_data)

                    prefix = "http://mamacdn.com/link.php?asad="
                    if url.startswith(prefix):
                        url = url.replace(prefix, "")
                        event_data = (int(time.time()), url, get_ip_address(url))
                        urls.add(event_data)

                    logger.debug("URL: {}".format(event_data))
            except (KeyError, socket.gaierror):
                continue
        return tuple({"timestamp": e[0], "url": e[1], "ip": e[2]} for e in urls)

    except AttributeError:
        return tuple()


def scrape():
    """Scrape mamahd.

    :return: A list of {"timestamp": _, "url": _, "ip": _}
    """
    all_urls = []
    page = requests.get(HOME)
    soup = BeautifulSoup(page.text, "html.parser")

    unique_urls = set()
    # Search through "Open Video" links
    for td in soup.find_all("td", class_="team"):
        for a in td.find_all("a"):
            try:
                url = a.attrs["href"]
                unique_urls.add(url)
            except KeyError:
                continue

    # Process all urls in parallel.
    with mp.Pool(mp.cpu_count()) as p:
        results = p.map(_scrape_event, unique_urls)
        for event_urls in results:
            all_urls.extend(url for url in event_urls)

    return all_urls
