import calendar
import logging
import os
import socket
from urllib.parse import urlparse

import geoip2.database
import psycopg2
from psycopg2 import IntegrityError
from selenium import webdriver

logger = logging.getLogger(__name__)

GCSQL_PWD = os.environ["GCSQL_PWD"]

dir_path = os.path.dirname(os.path.realpath(__file__))
reader = geoip2.database.Reader(dir_path + "/GeoLite2-Country.mmdb")


def get_geolocation(ip):
    """Return the geolocation of the IP based on GeoLite2 database."""
    response = reader.country(ip)

    return response.country.iso_code


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


def get_last_scanned(agg):
    """Get the last time urls were added to the postgres database.

    Because we are using Google CloudSQL, in order for this to work,
    you must first run "./cloud_sql_proxy \
    -instances=sports-streaming-security:us-west1:cs356-streams=tcp:6543 \
    -credential_file=sports-streaming-security-64e6f13735d5.json" in another
    terminal to set up port forwarding as required. Note that the second argument
    in this command is the authentication file containing the private key for the
    GCP instance, which you must get from Hudson.
    More information can be found in db_setup.txt, in this directory.


    :param agg: The name of the aggregator scanned
    :rtype: int
    """

    # TODO: Modify code to insert row if it isnt already present
    # TODO: Return errors if this fails
    conn = psycopg2.connect(
        host="localhost",
        port="6543",
        dbname="postgres",
        user="postgres",
        password=GCSQL_PWD,
    )
    cur = conn.cursor()
    select_cmd = "SELECT scanned FROM last_scan WHERE aggregator = '" + agg + "'"
    cur.execute(select_cmd)
    rows = cur.fetchall()
    last_time = rows[0][0]
    cur.close()
    conn.close()
    return calendar.timegm(last_time.timetuple())


def update_last_scanned(agg, scan_time):
    """Save the last time urls were added to the postgres database.

    Because we are using Google CloudSQL, in order for this to work,
    you must first run "./cloud_sql_proxy \
    -instances=sports-streaming-security:us-west1:cs356-streams=tcp:6543 \
    -credential_file=sports-streaming-security-64e6f13735d5.json" in another
    terminal to set up port forwarding as required. Note that the second argument
    in this command is the authentication file containing the private key for the
    GCP instance, which you must get from Hudson.
    More information can be found in db_setup.txt, in this directory.

    This function returns positive on success, negative on failure

    :param agg: The name of the aggregator scanned
    :param time: Unix timestamp of the last scan
    :rtype: int
    """

    # TODO: Modify code to insert row if it isnt already present
    # TODO: Return errors if this fails
    conn = psycopg2.connect(
        host="localhost",
        port="6543",
        dbname="postgres",
        user="postgres",
        password=GCSQL_PWD,
    )
    cur = conn.cursor()
    update_cmd = (
        "UPDATE last_scan SET " "(scanned)" "= (%s) WHERE aggregator = '" + agg + "'"
    )
    cur.execute(update_cmd, (psycopg2.TimestampFromTicks(scan_time),))
    conn.commit()
    cur.close()
    conn.close()
    return 0


def _get_base_url(url):
    o = urlparse(url)
    return o.netloc


def save_urls_to_db(urls, agg):
    """Save the passed list of URLs to the postgres database.

    Because we are using Google CloudSQL, in order for this to work,
    you must first run "./cloud_sql_proxy \
    -instances=sports-streaming-security:us-west1:cs356-streams=tcp:6543 \
    -credential_file=sports-streaming-security-64e6f13735d5.json" in another
    terminal to set up port forwarding as required. Note that the second argument
    in this command is the authentication file containing the private key for the
    GCP instance, which you must get from Hudson.
    More information can be found in db_setup.txt, in this directory.

    :param urls: A list of dictionaries containing the urls and associated info
    :param agg: The name of the aggregator scanned
    :rtype: int
    """
    conn = psycopg2.connect(
        host="localhost",
        port="6543",
        dbname="postgres",
        user="postgres",
        password=GCSQL_PWD,
    )
    cur = conn.cursor()
    add_url_cmd = (
        "INSERT INTO stream_urls "
        "(url, base_url, ip, country, aggregator, subreddit, reddit_user,"
        "mobile_compat, upvotes, created_on, last_access)"
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    update_cmd = (
        "UPDATE stream_urls SET "
        "(last_access, access_count)"
        "= (%s, %s) WHERE url = (%s)"
    )
    get_access_cnt_cmd = "SELECT access_count FROM stream_urls WHERE url = (%s)"

    if agg == "reddit":
        for url in urls:
            # TODO: Improve error handling for connection failures
            try:
                ip = get_ip_address(url.get("url"))
                country = get_geolocation(ip)
                cur.execute(
                    add_url_cmd,
                    (
                        url.get("url"),
                        _get_base_url(url.get("url")),
                        ip,
                        country,
                        agg,
                        url.get("subreddit"),
                        url.get("poster"),
                        url.get("mobile_compat"),
                        url.get("score"),
                        psycopg2.TimestampFromTicks(url.get("created")),
                        psycopg2.TimestampFromTicks(url.get("accessed")),
                    ),
                )
            except IntegrityError:
                # URL was already in db! Instead of insert, update access count
                conn.rollback()
                cur.execute(get_access_cnt_cmd, (url.get("url"),))
                rows = cur.fetchall()
                prev_count = rows[0]
                logger.debug("Detected a duplicate URL: " + url.get("url"))
                new_count = prev_count[0] + 1
                cur.execute(
                    update_cmd,
                    (
                        psycopg2.TimestampFromTicks(url.get("accessed")),
                        new_count,
                        url.get("url"),
                    ),
                )

            conn.commit()
    else:
        for url in urls:
            # `created_on` is meaningless in this context. Instead, it
            # represents the first access time.
            try:
                ip = get_ip_address(url.get("url"))
                country = get_geolocation(ip)
                cur.execute(
                    add_url_cmd,
                    (
                        url.get("url"),
                        _get_base_url(url.get("url")),
                        ip,
                        country,
                        agg,
                        None,
                        None,
                        None,
                        None,
                        psycopg2.TimestampFromTicks(url.get("timestamp")),
                        psycopg2.TimestampFromTicks(url.get("timestamp")),
                    ),
                )
            except IntegrityError:
                # URL was already in db! Instead of insert, update access count
                conn.rollback()
                cur.execute(get_access_cnt_cmd, (url.get("url"),))
                rows = cur.fetchall()
                prev_count = rows[0]
                logger.debug("Detected a duplicate URL: " + url.get("url"))
                new_count = prev_count[0] + 1
                cur.execute(
                    update_cmd,
                    (
                        psycopg2.TimestampFromTicks(url.get("timestamp")),
                        new_count,
                        url.get("url"),
                    ),
                )

            conn.commit()

    cur.close()
    conn.close()
    return 0
