import logging

from streamscrape.other import livetv


def test_scrape_event(caplog):
    """Just a passing test."""
    caplog.set_level(logging.INFO)

    livetv._scrape_event(
        "http://livetv.sx/enx/eventinfo/720950_atp_challenger_traralgon/"
    )


def test_scrape(caplog):
    """Just check that some urls are found."""
    caplog.set_level(logging.INFO)
    logger = logging.getLogger(__name__)
    results = livetv.scrape()
    logger.info("Total URLs: {}".format(len(results)))
