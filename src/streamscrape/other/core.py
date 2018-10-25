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

from streamscrape.other import livetv, rojadirecta

logger = logging.getLogger(__name__)


def scrape():
    """Core driver method for scraping other aggregator sites."""
    total_urls = []
    logger.info("Scraping http://livetv.sx")
    total_urls.extend(livetv.scrape())
    logger.info("Scraping http://www.rojadirecta.me")
    total_urls.extend(rojadirecta.scrape())
    return total_urls
