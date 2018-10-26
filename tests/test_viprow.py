import logging
from pprint import pformat

from streamscrape.other import viprow


def test_scrape(caplog):
    """Just check that some urls are found."""
    caplog.set_level(logging.INFO)
    logger = logging.getLogger(__name__)
    results = viprow.scrape()
    logger.info("{}".format(pformat(results)))
    logger.info("Total URLs: {}".format(len(results)))
