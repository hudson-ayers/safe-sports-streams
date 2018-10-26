"""This is the core library for scraping the top aggregator sites we study.

Specifically, we look at:
    - http://livetv.sx/
    - http://www.rojadirecta.me/
    - https://www.stream2watch.org/
    - https://www.livesoccertv.com/
    - http://cricsports.sc/
    - https://www.jokerlivestream.com
    - http://www.fromhot.com/
    - https://www.viprow.net/
    - http://firstrowonly.eu/
    - https://www.batmanstream.net/
"""

import logging

from streamscrape.other import (
    cricsports,
    firstrow,
    fromhot,
    livetv,
    rojadirecta,
    stream2watch,
    viprow,
)

logger = logging.getLogger(__name__)


def scrape():
    """Core driver method for scraping other aggregator sites."""
    total_urls = []
    logger.info("Scraping http://livetv.sx")
    total_urls.extend(livetv.scrape())
    logger.info("Scraping http://www.rojadirecta.me")
    total_urls.extend(rojadirecta.scrape())
    logger.info("Scraping https://www.stream2watch.org")
    total_urls.extend(stream2watch.scrape())
    logger.info("Scraping http://cricsports.sc")
    total_urls.extend(cricsports.scrape())
    logger.info("Scraping http://firstrowonly.eu")
    total_urls.extend(firstrow.scrape())
    logger.info("Scraping http://www.fromhot.com")
    total_urls.extend(fromhot.scrape())
    logger.info("Scraping https://www.viprow.net")
    total_urls.extend(viprow.scrape())
    return total_urls
