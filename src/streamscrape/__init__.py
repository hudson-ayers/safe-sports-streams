import logging

from streamscrape._version import __version__

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ["__version__"]
