import random

from basegooglescrapper import BaseGoogleScrapper


class SimpleGoogleSearchScrapper(BaseGoogleScrapper):
    """Scrapper for scrapping and parsing google search results."""

    def _get_keywords(self, filename, no_of_keywords, *args, **kwargs):
        """Get keywords from the text file."""
        text_file = open(filename, 'r')
        return [text_file.readline() for _ in range(no_of_keywords)]


class GeoGoogleSearchScrapper(BaseGoogleScrapper):
    """Scrapper for scrapping and parsing google search results."""

    def _get_keywords(self, filename, *args, **kwargs):
        """Get a random keyword from the text file."""
        keywords = super()._get_keywords(filename)
        return [random.choice(keywords)]
