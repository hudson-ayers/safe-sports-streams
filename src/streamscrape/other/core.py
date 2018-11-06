"""This is the core library for scraping the top aggregator sites we study.

Specifically, we look at:
    - http://livetv.sx/
    - http://www.rojadirecta.me/
    - https://www.stream2watch.org/
    - http://cricsports.sc/
    - http://www.fromhot.com/
    - https://www.viprow.net/
    - http://firstrowonly.eu/
    - https://www.mamahd.org/
"""

import logging

from streamscrape.other import (
    cricsports,
    firstrow,
    fromhot,
    livetv,
    mamahd,
    rojadirecta,
    stream2watch,
    viprow,
)

logger = logging.getLogger(__name__)


def scrape():
    """Core driver method for scraping other aggregator sites."""
    total_urls = []
    logger.info("Scraping http://livetv.sx")
    total_urls.append({"livetv": livetv.scrape()})
    logger.info("Scraping http://www.rojadirecta.me")
    total_urls.append({"rojadirecta": rojadirecta.scrape()})
    logger.info("Scraping https://www.stream2watch.org")
    total_urls.append({"stream2watch": stream2watch.scrape()})
    logger.info("Scraping http://cricsports.sc")
    total_urls.append({"cricsports": cricsports.scrape()})
    logger.info("Scraping http://firstrowonly.eu")
    total_urls.append({"firstrow": firstrow.scrape()})
    logger.info("Scraping http://www.fromhot.com")
    total_urls.append({"fromhot": fromhot.scrape()})
    logger.info("Scraping https://www.viprow.net")
    total_urls.append({"viprow": viprow.scrape()})
    logger.info("Scraping https://www.mamahd.org")
    total_urls.append({"mamahd": mamahd.scrape()})
    return total_urls
