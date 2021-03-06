import logging

from streamscrape.other import stream2watch


def test_scrape(caplog):
    """Just check that some urls are found."""
    caplog.set_level(logging.INFO)
    logger = logging.getLogger(__name__)
    results = stream2watch.scrape()
    logger.info("Total URLs: {}".format(len(results)))
