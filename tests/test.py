import requests
from urllib import parse
import mimetypes


def is_image_url(url):    
    mimetype,encoding = mimetypes.guess_type(url)
    print(mimetype)
    return (mimetype and (mimetype.startswith('image') or mimetype.startswith('text/css')))

def read_file(filename):
    with open(filename) as f:
        content = f.read()
        print('1')
        print(content)



url='https://octoverse.github.com/static/github-octoverse-2020-productivity-report.pdf#page=10'

v = parse.urlparse(url).path
print(v)
print(is_image_url(v))
#read_file('/home/arshad/workspace/bounty/crawl4takeover/output.txt')
