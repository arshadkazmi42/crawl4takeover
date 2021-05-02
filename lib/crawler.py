from bs4 import BeautifulSoup

from .helper import Helper

from config import global_config


class Crawler:
    
    def __init__(self):

        self.urls = {}
        self.links = []

        self.start_url = Helper.get_url()

        self.urls[self.start_url] = False
        self.links.append(self.start_url)

        Helper.init(self.start_url)


    def start_scan(self):

        for url in self.links:

            print_line = f'Scanning for {url}'
            print(print_line)
            Helper.write_to_file(global_config['file_names']['process'], print_line)

            response = Helper.get_url_result(url)

            if response:

                Helper.parse_urls_with_regex(response, self.urls, self.links)

                try:
                    soup = BeautifulSoup(response, 'html.parser')

                    link_tags = global_config['tags']['link']
                    image_tags = global_config['tags']['image']

                    Helper.parse_urls(soup, link_tags, self.urls, self.links)
                    Helper.parse_urls(soup, image_tags, self.urls)
                except Exception as e:
                    print(f'Exception while scanning url {url}', e)
                    
