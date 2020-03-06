from basegooglescrapper import BaseGoogleScrapper


class SimpleGoogleSearchScrapper(BaseGoogleScrapper):
    """Scrapper for scrapping and parsing google search results."""

    def _get_keywords(self, filename, no_of_keywords):
        """Get keywords from the text file."""
        text_file = open(filename, 'r')
        return [text_file.readline() for _ in range(no_of_keywords)]