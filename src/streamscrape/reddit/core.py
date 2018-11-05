#!/usr/bin/env python3

import argparse
import logging
import os
import re
import time

import praw

PERSONAL_USE_SCRIPT = os.environ["SPORTS_STREAMER_PUS"]
SCRAPER_SECRET = os.environ["SPORTS_STREAMS_SCRAPER_SECRET"]
REDDIT_PASSWORD = os.environ["REDDIT_PASSWORD"]
log = logging.getLogger(__name__)

# List of streaming subreddits
STREAMING_SUBREDDITS = [
    "nbastreams",
    "soccerstreams",
    "nflstreams",
    "cfbstreams",
    "ncaabballstreams",
    "puttstreams",
    "nhlstreams",
    "mlbstreams",
    "cricketstreams",
    "rugbystreams",
    "mmastreams",
    "boxingstreams",
    "wwestreams",
    "motorsportsstreams",
]

# Design: We store all URLS in a list of dictionaries where each dictionary contains
# metadata associated with that URL

# Default operation scrapes all streaming subreddits, categorizes
# links along with author, subreddit, verified tag, ad overlays, upvotes, time posted,
# mobile compatibly


def find_urls(string):
    # findall() has been used
    # with valid conditions for urls in string
    urls = re.findall(r"(?=\(http).+(?=\))", string)
    urls_cleaned = []
    for url in urls:
        # remove leading paren
        url = url[1:]
        # sometimes the regex misses the closing paren, below code fixes
        if ")" in url:
            url = url[: url.index(")")]
        urls_cleaned.append(url)
    return urls_cleaned


def check_if_game_thread(submission):
    # For example, nbastreams always prefaces with "game thread",
    # but soccerstreams merely lists the teams and game time in brackets.
    if (
        "game thread" in submission.title.lower()
        or " vs " in submission.title.lower()
        or " v " in submission.title.lower()
    ):
        return True
    elif (
        submission.subreddit.display_name == "motorsportsstreams"
        and "[" in submission.title.lower()
    ):
        return True
    else:
        return False


def scrape_subreddit(subreddit_name, num_posts, last_scrape_time=0):
    if subreddit_name not in STREAMING_SUBREDDITS:
        log.warn(subreddit_name + " is not a known streaming subreddit.")
        return []
    log.info("scraping:" + subreddit_name)
    url_list = []
    reddit = praw.Reddit(
        client_id=PERSONAL_USE_SCRIPT,
        client_secret=SCRAPER_SECRET,
        user_agent="sports-streams-scraper",
        username="cs356",
        password=REDDIT_PASSWORD,
    )

    subreddit = reddit.subreddit(subreddit_name)
    hot_subreddit = subreddit.hot(limit=num_posts)
    cur_time = float(time.time())
    # Parse data from individual posts
    for submission in hot_subreddit:
        # By default, skip all posts more than 2 days (172800 seconds) old
        # If last scrape time is known, ignore all posts that preceded it
        if last_scrape_time == 0:
            log.info("No last scrape time provided.")
            last_scrape_time = cur_time - 172800
        if submission.created_utc < last_scrape_time:
            continue
        # First, check that the submission is a game thread.
        if check_if_game_thread(submission):
            submission.comments.replace_more(limit=0)  # remove "more comments" links
            for top_level_comment in submission.comments:
                # skip removed comments
                if (
                    top_level_comment.body == "[removed]"
                    or top_level_comment.body == "[deleted]"
                ):
                    continue
                urls = find_urls(top_level_comment.body)

                if urls:
                    # Collect data on the post to associate with these URLs
                    # TODO: Check flair, overlay count
                    if not top_level_comment.author:
                        log.warn("This comment has no author:" + top_level_comment.body)
                        name = ""
                    else:
                        name = top_level_comment.author.name

                    # Check if stream supports mobile (if not listed, assume no)
                    # Comments sometimes say yes mobile or mobile:yes etc.
                    # Compatibility levels:
                    #  -1: No statement on compatibility
                    #  0: No compatibility
                    #  1: Android only compatibility
                    #  2: Ios only compatibility
                    #  3: Full compatibility

                    mobile_compat = -1
                    mobile_spot = top_level_comment.body.lower().find("mobile")
                    if mobile_spot != -1:
                        if (
                            "yes"
                            in top_level_comment.body.lower()[
                                mobile_spot - 5 : mobile_spot + 26
                            ]
                        ):
                            mobile_compat = 3
                        elif (
                            "no"
                            in top_level_comment.body.lower()[
                                mobile_spot - 5 : mobile_spot + 26
                            ]
                        ):
                            mobile_compat = 0
                        elif (
                            "android"
                            in top_level_comment.body.lower()[
                                mobile_spot - 5 : mobile_spot + 26
                            ]
                        ):
                            mobile_compat = 1
                        elif (
                            "ios"
                            in top_level_comment.body.lower()[
                                mobile_spot - 5 : mobile_spot + 26
                            ]
                        ):
                            mobile_compat = 2
                        else:
                            # Probably just a statement like "mobile compatible"
                            log.debug(
                                "Misunderstood mobile compat for "
                                + top_level_comment.body
                            )
                            mobile_compat = 3

                    for url in urls:
                        url_dict = {
                            "url": url,
                            "created": top_level_comment.created_utc,
                            "accessed": cur_time,
                            "subreddit": subreddit_name,
                            "poster": name,
                            "score": top_level_comment.score,
                            # "verified": ??,
                            "mobile": mobile_compat,
                            # "overlay_count": ??,
                        }
                        url_list.append(url_dict)
                        log.debug(url_dict)

                else:
                    log.debug("No URLs in " + top_level_comment.body)
        else:
            log.debug(submission.title + ": Is not a game thread.")
    return url_list


def scrape_all(num_posts, last_scrape_time=0):
    all_urls = []
    no_streams_list = []
    found_streams_count = []
    for subreddit_name in STREAMING_SUBREDDITS:
        urls = scrape_subreddit(subreddit_name, num_posts, last_scrape_time)
        if not urls:
            no_streams_list.append(subreddit_name)
        else:
            found_streams_count.append((subreddit_name, len(urls)))
            all_urls.extend(urls)
    log.info(
        "The following subreddits have no new streams active: " + str(no_streams_list)
    )
    print(
        "The number of new streams found for each other subreddit: "
        + str(found_streams_count)
    )
    return all_urls


def main():
    # This main method can be used for scraping single subreddits
    parser = argparse.ArgumentParser()
    parser.add_argument("subreddit_name", help="name of the subreddit to scrape")
    parser.add_argument(
        "--num_posts",
        type=int,
        default=50,
        help="How many of the hot posts on the subreddit to scrape",
    )
    subreddit_name = parser.parse_args().subreddit_name
    num_posts = parser.parse_args().num_posts

    scrape_subreddit(subreddit_name, num_posts)


if __name__ == "__main__":
    main()
