import requests
from bs4 import BeautifulSoup


class PaginatedScrapper:
    URL = 'https://www.guestpostengine.com/search?q=health&page='
    PAGE_THRESHOLD = 10

    def parse(self, content):
        """Parse page content."""
        soup = BeautifulSoup(content, "html.parser")
        results = []
        for div in soup.find_all('div', class_='kt-portlet__body'):

            domain_name = div.find('a', class_='kt-widget__username')
            if not domain_name:
                continue
            detail_dict = {}
            detail_dict['domain_name'] = domain_name.text.strip()
            details = div.find_all('div', class_='kt-widget__item')

            for detail in details:
                key = detail.find(
                    'span', class_='kt-widget__title'
                ).text.strip()
                value = detail.find(
                    'span', class_='kt-widget__value'
                ).text.strip()
                detail_dict[key] = value
            results.append(detail_dict)
        return results

    def get_page_content(self, page_number):
        """Get Page results."""
        url = self.URL + str(page_number)
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.HTTPError('An error occurred.')
        return response.content

    def run(self):
        """Get google search results in a Dict."""
        results = []
        for page_number in range(1, self.PAGE_THRESHOLD + 1):
            content = self.get_page_content(page_number)
            results.extend(self.parse(content))
        return results
