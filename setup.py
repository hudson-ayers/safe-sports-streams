"""For pip."""
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

exec(open("src/streamscrape/_version.py").read())
setup(
    name="streamscrape",
    version=__version__,
    description="Scrape for live sport stream URLs.",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    install_requires=[
        "beautifulsoup4",
        "praw",
        "requests",
        "selenium",
        "psycopg2",
        "geoip2",
    ],
    include_package_data=True,
    keywords=["scraping", "streams"],
    scripts=["bin/scrape_aggregators", "bin/scrape_reddit"],
    url="https://github.com/hudson-ayers/safe-sports-streams",
    classifiers=[  # https://pypi.python.org/pypi?:action=list_classifiers
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    project_urls={
        "Tracker": "https://github.com/hudson-ayers/safe-sports-streams/issues",
        "Source": "https://github.com/hudson-ayers/safe-sports-streams",
    },
    python_requires=">=3.6",
    author="Hudson Ayers",
    author_email="",
    license="MIT",
)
