import re
import requests
import sys
import mimetypes
from pathlib import Path
from urllib import parse

from config import global_config


class Helper:


    @classmethod
    def set_start_url(cls, url):
        cls.start_url = url


    @classmethod
    def print(cls, value): 
        if global_config['debug']:
            print(value)


    @classmethod
    def clean_url(cls, url):

        url = url.replace('\'', '')
        url = url.replace('"', '')
        url = url.replace('&quot', '')

        return url


    @classmethod
    def get_url(cls):

        args = sys.argv

        if len(args) < 2:
            print('You should pass the URL to the script in command line parameter')
            print('Eg: python scan.py [YOUR_URL]')
            exit()

        return args[1]


    @classmethod
    def get_url_result(cls, url):

        cls.print(url)
        try:

            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                cls.print(f'Failed with error code {response.status_code}')
                return
                
            return response.text

        except:
            cls.print(f'Error making request call to {url}')
            return


    @classmethod
    def get_status_code(cls, url):
        try:
            response = requests.get(url, timeout=10)
            return response.status_code
        except:
            cls.print(f'Error getting status code of {url}')
            return


    @classmethod
    def parse_urls(cls, hostname, soup, tags, urls, links=None):

        for tag in tags:

            for link in soup.find_all(tag):

                url = link.get(tags[tag])
                cls.process_link(hostname, url, urls, links)


    @classmethod
    def parse_urls_with_regex(cls, text, hostname, urls, links):

        regex = global_config['regex']['link']
        matches = [x.group() for x in re.finditer(regex, text)]

        cls.print(matches)

        for i in range(0, len(matches)):
            url = matches[i]
            cls.process_link(hostname, url, urls, links)


    @classmethod
    def process_link(cls, hostname, url, urls, links):

        cls.print(url)

        valid_url = cls.validate_and_write(hostname, url)

        cls.print(valid_url)

        if valid_url:
            if valid_url not in urls.keys():
                urls[valid_url] = False
            
            if links and valid_url.startswith(cls.start_url) and valid_url not in links and not cls.is_media_url(valid_url):
                links.append(valid_url)    


    @classmethod
    def validate_and_write(cls, hostname, url):

        if not url:
            return None

        # Remove starting and ending quotes
        url = cls.clean_url(url)

        if url.startswith('javascript:') or url.startswith('mailto:') or url.startswith('#'):
            return None

        if not url.startswith('http'):
            url = cls.merge_url_path(cls.start_url, url)

        cls.print(f'Valid URL: {url}')

        if global_config['filters']['enable']:
            for value in global_config['filters']['tags']:
                if value in url:
                    cls.capture_url(hostname, url)
        else:
            cls.capture_url(hostname, url)

        return url

    
    @classmethod
    def capture_url(cls, hostname, url):

        status_code = cls.get_status_code(url)

        if status_code == 404:
            cls.print('\n========== FOUND BROKEN LINK => TAKEOVER MIGHT BE POSSIBLE =========\n')
            cls.print(f'{url} => {status_code}')
            cls.print('\n===================\n')

        if status_code == 404:
            print(f'|-BROKEN-| {url}')
            cls.write_to_file(hostname, global_config['file_names']['broken_links'], url)
        else:
            print(f'|---OK---| {url}')
            cls.write_to_file(hostname, global_config['file_names']['all_links'], url)   


    @classmethod
    def write_to_file(cls, foldername, filename, line):

        directory = f'{global_config["directories"]["results"]}/{foldername}'
        file_path = f'{directory}/{filename}'

        # check if line already present in file
        if cls.is_file_exists(file_path):
            with open(file_path) as f:
                file_content = f.read()
                if line in file_content:
                    cls.print('\n\nLINE EXISTSS\n\n')
                    return

        f = open(file_path, 'a')
        f.write(f'{line}\n')  # python will convert \n to os.linesep
        f.close()


    @classmethod
    def is_file_exists(cls, file_path):
        fyle = Path(file_path)
        if fyle.is_file():
            return True
        return False


    @classmethod
    def is_media_url(cls, url):
        # Check mimetype for path
        # As sometimes URL have some get parameter
        # Due to which mimetype is not returned properly
        mime_types = global_config['mime_types']['media']
        url_path = cls.parse_url_path(url)
        mimetype,encoding = mimetypes.guess_type(url_path)
        return (mimetype and (mimetype.startswith(tuple(mime_types))))

    
    @classmethod
    def parse_url_path(cls, url):
        
        if not url:
            return

        return parse.urlparse(url).path


    @classmethod
    def get_hostname(cls, url):

        # Hostname will be used to identify next page urls of same domain
        hostname = parse.urlparse(url).hostname
        hostname = hostname.split('.')
        if len(hostname) > 1:
            return f'{hostname[len(hostname) - 2]}.{hostname[len(hostname) - 1]}'
        
        return

    
    @classmethod
    def merge_url_path(cls, url, path):

        if url.endswith('/') and path.startswith('/'):
            return f'{url}{path[1:]}'
        elif not url.endswith('/') and path.startswith('/'):
            return f'{url}{path}'
        elif url.endswith('/') and not path.startswith('/'):
            return f'{url}{path}'
        else:
            return f'{url}/{path}'

    
    @classmethod
    def create_results_directory(cls, hostname):

        # Create directory for the host if not exists
        directory = f'{global_config["directories"]["results"]}/{hostname}'
        Path(directory).mkdir(parents=True, exist_ok=True)

