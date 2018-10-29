import logging
import os
import socket
from datetime import datetime
from urllib.parse import urlparse

import psycopg2
from selenium import webdriver

logger = logging.getLogger(__name__)

GCSQL_PWD = os.environ["GCSQL_PWD"]


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
    :raises: socket.gaierror if the name/protocol is unknown
    """
    parsed_uri = urlparse(url)
    try:
        ip = socket.gethostbyname(parsed_uri.netloc)
        return ip
    except Exception as e:
        logger.error("URL: {} error with {}".format(url, e))
        raise


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


def save_urls_to_db(urls):
    """Save the passed list of URLs to the postgres database.

    Because we are using Google CloudSQL, in order for this to work,
    you must first run "./cloud_sql_proxy \
    -instances=sports-streaming-security:us-west1:cs356-streams=tcp:6543 \
    -credential_file=sports-streaming-security-64e6f13735d5.json" in another
    terminal to set up port forwarding as required. Note that the second argument
    in this command is the authentication file containing the private key for the
    GCP instance, which you must get from Hudson.
    More information can be found in db_setup.txt, in this directory.

    :param url_info: A list of dictionaries containing the urls and associated info
    :rtype: int
    """
    conn = psycopg2.connect(
        host="localhost",
        port="6543",
        database="stream_urls",
        user="postgres",
        password=GCSQL_PWD,
    )
    cur = conn.cursor()
    add_url_cmd = (
        "INSERT INTO stream_urls "
        "(url, base_url, aggregator, subreddit, reddit_user,"
        "mobile_compat, upvotes, created_on, last_access)"
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    for url in urls:
        # TODO: Check if URL was already in database, and if so increment count
        # TODO: Error handling, catch exceptions, etc.
        # TODO: Get Base URL correctly
        # TODO: Make this not reddit specific
        cur.execute(
            add_url_cmd,
            (
                url.get("url"),
                url.get("url"),
                "reddit",
                url.get("subreddit"),
                url.get("poster"),
                url.get("mobile_compat"),
                url.get("score"),
                psycopg2.TimestampFromTicks(url.get("created")),
                psycopg2.TimestampFromTicks(url.get("accessed")),
            ),
        )
        conn.commit()
    cur.close()
    conn.close()
    return 0
