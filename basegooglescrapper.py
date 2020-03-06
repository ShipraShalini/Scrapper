import urllib.parse

import requests

from bs4 import BeautifulSoup


class BaseGoogleScrapper:
    """Scrapper for scrapping and parsing google search results."""

    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    TARGET_DOMAIN = 'amazon.in'

    def get_google_results(self, keyword):
        """Get google results."""
        url = self._get_google_url(keyword)
        response = requests.get(url,
                                headers={"user-agent": self.USER_AGENT})
        if response.status_code != 200:
            raise requests.HTTPError('An error occurred.')
        return response.content

    def parse(self, content, domain_to_search):
        """Parse google response."""
        soup = BeautifulSoup(content, "html.parser")
        results = []
        domain_position = -1
        for idx, div in enumerate(soup.find_all('div', class_='rc')):
            a = div.find_all('a')
            if a:
                idx += 1
                link = a[0]['href']
                domain = self.get_domain(link)
                title = div.find('h3').text
                desc = div.find('span', class_='st').text
                results.append({
                    'link': link,
                    'domain': domain,
                    'title': title,
                    'desc': desc,
                    'position': idx
                })
                if domain == domain_to_search:
                    domain_position = idx
        return {'results': results, 'domain_position': domain_position}

    def run(self, filename, no_of_keywords):
        """Get google search results in a Dict."""
        keywords = self._get_keywords(filename, no_of_keywords)
        results = {}
        for keyword in keywords:
            content = self.get_google_results(keyword)
            results[keyword] = self.parse(content, self.TARGET_DOMAIN)
        return results

    def get_domain(self, link):
        """Get the domain name."""
        return urllib.parse.urlparse(link).netloc

    def _get_keywords(self, filename, no_of_keywords):
        """Get keywords from the text file."""
        text_file = open(filename, 'r')
        return [line.strip() for line in text_file.readlines()]

    def _get_google_url(self, keyword):
        """Construct the final Google URL."""
        keyword = urllib.parse.quote_plus(keyword)
        return f"https://google.com/search?q={keyword}"


