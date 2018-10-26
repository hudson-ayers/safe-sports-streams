import logging
import socket
from datetime import datetime
from urllib.parse import urlparse

from selenium import webdriver

logger = logging.getLogger(__name__)


def get_utc_time_str():
    """Return the current UTC time as a string.

    :return: The current UTC time.
    :rtype: str
    """
    return str(datetime.utcnow())


def get_ip_address(url):
    """Return the IPv4 address of the given URL.

    :param url: The string URL to parse.
    :return: The IPv4 address of the hostname.
    :rtype: str
    """
    parsed_uri = urlparse(url)
    try:
        ip = socket.gethostbyname(parsed_uri.netloc)
        return ip
    except Exception as e:
        logger.error("URL: {}".format(url))
        logger.error(e)
        return "N/A"


def get_chrome_webdriver():
    """Return a headless Chrome webdriver.

    The caller is in charge of calling quit() on this driver so that there are
    not chrome processes leftover after a run.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    # This window size is arbitrary. But, seems like it captures a good area
    # if you wanted to screenshot the page.
    options.add_argument("window-size=1200x800")
    driver = webdriver.Chrome(options=options)

    return driver
