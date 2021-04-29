import re
import requests
import base64
import json
import sys
import mimetypes
from bs4 import BeautifulSoup
from urllib import parse

DEBUG = False
# Enable to filter urls by this list FILTER_URLS
ENABLE_FILTER = True
FILENAME = 'output.txt'
BROKEN_LINKS_FILENAME = 'broken.txt'
REGEX = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9]{1,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)'
MIME_TYPES = ['audio', 'video', 'image']
LINK_TAGS = { 'a': 'href', 'link': 'href', 'script': 'src' }
IMAGE_TAGS = {'img': 'src'}
FILTER_URLS = [ 'amazonaws', 'herokuapp', 'netlify', 'storage.googleapis.com', 'github', 'zendesk' ]



# HELPER FUNCTIONS

def _print(text):
    # TODO Add debug / verbose flag / accept from arg
    if DEBUG:
        print(text)


# URL should be passed as first parameter to the script
def _get_url():
    args = sys.argv

    if len(args) < 2:
        print('You should pass the URL to the script in command line parameter')
        print('Eg: python scan.py [YOUR_URL]')
        exit()

    return args[1]


def _get_url_result(url):

    _print(url)
    try:

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            _print(f'Failed with error code {response.status_code}')
            return
            
        return response.text

    except:
        _print(f'Error making request call to {url}')
        return


def _clean_url(url):
    url = url.replace('\'', '')
    url = url.replace('"', '')

    return url


def _get_status_code(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code
    except:
        _print(f'Error getting status code of {url}')
        return


def _validate_and_write(url):

    if not url:
        return None

    # Remove starting and ending quotes
    url = _clean_url(url)

    if not url.startswith('http'):
        return None

    if url.startswith('javascript:'):
        return None

    _print(f'Valid URL: {url}')

    if ENABLE_FILTER:
        for value in FILTER_URLS:
            if value in url:
                _capture_url(url)
    else:
        _capture_url(url) 

    return True


def _capture_url(url):

    status_code = _get_status_code(url)

    if status_code == 404:
        _print('\n========== FOUND BROKEN LINK => TAKEOVER MIGHT BE POSSIBLE =========\n')
        print(f'{url} => {status_code}')
        _print('\n===================\n')

    if status_code == 404:
        _write_to_file(BROKEN_LINKS_FILENAME, url)
    else:
        _write_to_file(FILENAME, url)


def _parse_urls(soup, hostname, tags, urls, links=None):

    for tag in LINK_TAGS:

        for link in soup.find_all(tag):

            url = link.get(LINK_TAGS[tag])
            _process_link(hostname, url, urls, links)


def _parse_urls_with_regex(text, hostname, urls, links):

    matches = [x.group() for x in re.finditer(REGEX, text)]
    _print(matches)

    for i in range(0, len(matches)):
        url = matches[i]
        _process_link(hostname, url, urls, links)


def _process_link(hostname, url, urls, links):

    _print(url)

    is_valid = _validate_and_write(url)

    if is_valid:
        if url not in urls.keys():
            urls[url] = False
        
        if links and hostname in url and url not in links and not is_media_url(url):
            links.append(url)       


def _write_to_file(filename, line):
    f = open(f'{filename}', 'a')
    f.write(f'{line}\n')  # python will convert \n to os.linesep
    f.close()

def is_media_url(url):
    # Check mimetype for path
    # As sometimes URL have some get parameter
    # Due to which mimetype is not returned properly
    url_path = parse.urlparse(url).path
    mimetype,encoding = mimetypes.guess_type(url_path)
    return (mimetype and (mimetype.startswith(tuple(MIME_TYPES))))

def _start_scan(hostname, urls, links):

    for url in links:

        print(f'Scanning for {url}')

        response = _get_url_result(url)

        if response:

            _parse_urls_with_regex(response, hostname, urls, links)

            try:
                soup = BeautifulSoup(response, 'html.parser')

                _parse_urls(soup, hostname, LINK_TAGS, urls, links)
                _parse_urls(soup, hostname, IMAGE_TAGS, urls)
            except:
                _print(f'Exception while scanning url {url}')


# MAIN CODE
urls = {}
links = []
index = 0

start_url = _get_url()
urls[start_url] = False
links.append(start_url)

# Hostname will be used to identify next page urls of same domain
hostname = parse.urlparse(start_url).hostname
hostname = hostname.split('.')
if len(hostname) > 1:
    hostname = f'{hostname[len(hostname) - 2]}.{hostname[len(hostname) - 1]}'


_start_scan(hostname, urls, links)
