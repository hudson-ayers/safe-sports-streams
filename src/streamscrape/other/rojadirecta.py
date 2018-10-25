"""Code for scraping from RojaDirecta."""
import logging

import requests
from bs4 import BeautifulSoup

from streamscrape.utils import get_ip_address, get_utc_time_str

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

        event_data = (get_utc_time_str(), href, get_ip_address(href))
        logger.debug("RojaDirecta URL data: {}".format(event_data))
        all_urls.append(event_data)

    return all_urls

    #  def scrape():
    #      """Scrape LiveTV.
    #
    #      :return: A list of {"timestamp": _, "url": _, "ip": _}
    #      """
    #      page = requests.get(HOME)
    #      soup = BeautifulSoup(page.text, "html.parser")
    #
    #      # Gather current live URLs from the English ("enx") version of the page.
    #      live_urls = set(a.attrs["href"] for a in soup.find_all("a", class_="live"))
    #
    #      import pdb
    #
    #      pdb.set_trace()

    #
    #  all_urls = []
    #
    #  # Process all urls in parallel.
    #  with mp.Pool(2 * mp.cpu_count()) as p:
    #      results = p.map(_scrape_event, live_urls)
    #      for event_urls in results:
    #          all_urls.extend(url for url in event_urls)
    #
    #  logger.debug("{}".format(pformat(all_urls)))

    return
