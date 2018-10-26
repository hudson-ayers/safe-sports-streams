import logging

from streamscrape.other import cricsports


def test_scrape_event():
    cricsports._scrape_event(
        "http://cricsports.sc/watch/live/uefa-europa-league-simulcast-live-streaming"
    )


def test_scrape(caplog):
    """Just check that some urls are found."""
    caplog.set_level(logging.INFO)
    logger = logging.getLogger(__name__)
    results = cricsports.scrape()
    logger.info("Total URLs: {}".format(len(results)))
