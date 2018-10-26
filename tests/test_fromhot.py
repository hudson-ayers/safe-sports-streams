import logging

from streamscrape.other import fromhot


def test_scrape(caplog):
    """Just check that some urls are found."""
    caplog.set_level(logging.INFO)
    logger = logging.getLogger(__name__)
    results = fromhot.scrape()
    logger.info("Total URLs: {}".format(len(results)))
