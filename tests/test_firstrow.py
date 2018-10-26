import logging

from streamscrape.other import firstrow


def test_scrape(caplog):
    """Just check that some urls are found."""
    caplog.set_level(logging.INFO)
    logger = logging.getLogger(__name__)
    results = firstrow.scrape()
    logger.info("Total URLs: {}".format(len(results)))
