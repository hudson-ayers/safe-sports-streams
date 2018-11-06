"""Code for scraping from LiveTV."""
import logging
import multiprocessing as mp
import time

import requests
from bs4 import BeautifulSoup

from streamscrape.utils import get_chrome_webdriver, get_ip_address

logger = logging.getLogger(__name__)

LIVETV_HOME = "http://livetv.sx"


def _scrape_event(url):
    """Scrape a particular event URL.

    :param url: The LiveTV Event URL to scrape for browser links.
    :type url: string
    :return: A tuple of dict {"timestamp": _, "url": _, "ip": _}
    """
    event_urls = set()
    logger.debug("Scraping: {}".format(url))
    driver = get_chrome_webdriver()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links_table = soup.find(id="links_block")

    # remove header table, if present
    try:
        links_table.find(class_="lnkhdr").decompose()
    except AttributeError:
        # If no link table is present, just return an empty tuple
        driver.quit()
        return tuple()

    for link in [a.attrs["href"] for a in links_table.find_all("a")]:
        # Skip this URLs like ads/acestream
        if any(s in link for s in ["#null", "unibet", "acestream", "sop"]):
            continue

        # Append http if it is missing. livetv does not use HTTPS.
        if link.startswith("//"):
            link = "http:" + link

        event_data = (int(time.time()), link, get_ip_address(link))
        logger.debug("LiveTV URL data: {}".format(event_data))
        event_urls.add(event_data)

    driver.quit()
    return tuple({"timestamp": e[0], "url": e[1], "ip": e[2]} for e in event_urls)


def scrape():
    """Scrape LiveTV.

    :return: A list of {"timestamp": _, "url": _, "ip": _}
    """
    page = requests.get(LIVETV_HOME)
    soup = BeautifulSoup(page.text, "html.parser")

    # Gather current live URLs from the English ("enx") version of the page.
    live_urls = set(
        LIVETV_HOME + "/enx" + a.attrs["href"]
        for a in soup.find_all("a", class_="live")
    )

    all_urls = []

    # Process all urls in parallel.
    with mp.Pool(mp.cpu_count()) as p:
        results = p.map(_scrape_event, live_urls)
        for event_urls in results:
            all_urls.extend(url for url in event_urls)

    return all_urls
