import logging
from pprint import pformat

from streamscrape.other import mamahd


def test_scrape_event():
    mamahd._scrape_event(
        "https://www.mamahd.org/2.-Bundesliga-Magdeburg-vs-Hamburger-SV-live-stream/"
    )


def test_scrape(caplog):
    """Just check that some urls are found."""
    caplog.set_level(logging.INFO)
    logger = logging.getLogger(__name__)
    results = mamahd.scrape()
    logger.info("{}".format(pformat(results)))
    logger.info("Total URLs: {}".format(len(results)))
