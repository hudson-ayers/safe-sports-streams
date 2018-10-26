import logging
from pprint import pformat

from streamscrape.other import firstrow


def test_scrape(caplog):
    """Just check that some urls are found."""
    caplog.set_level(logging.DEBUG)
    logger = logging.getLogger(__name__)
    results = firstrow.scrape()
    logger.info("{}".format(pformat(results)))
