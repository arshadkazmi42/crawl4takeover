from bs4 import BeautifulSoup

from .helper import Helper

from config import global_config


class Crawler:
    
    def __init__(self):

        self.urls = {}
        self.links = []

        self.start_url = Helper.get_url()
        self.hostname = Helper.get_hostname(self.start_url)

        self.urls[self.start_url] = False
        self.links.append(self.start_url)

        Helper.set_start_url(self.start_url)
        Helper.create_results_directory(self.hostname)


    def start_scan(self):

        for url in self.links:

            print(f'Scanning for {url}')

            response = Helper.get_url_result(url)

            if response:

                Helper.parse_urls_with_regex(response, self.hostname, self.urls, self.links)

                # try:
                soup = BeautifulSoup(response, 'html.parser')

                link_tags = global_config['tags']['link']
                image_tags = global_config['tags']['image']

                Helper.parse_urls(self.hostname, soup, link_tags, self.urls, self.links)
                Helper.parse_urls(self.hostname, soup, image_tags, self.urls)
                # except:
                    # Helper.print(f'Exception while scanning url {url}')
