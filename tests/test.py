import requests
from urllib import parse
import mimetypes


def is_image_url(url):    
    mimetype,encoding = mimetypes.guess_type(url)
    print(mimetype)
    return (mimetype and (mimetype.startswith('image') or mimetype.startswith('video')))


url='https://magicleap.com/assets/fonts/lomino/lomino-bold.woff'
v = parse.urlparse(url).path
print(v)
print(is_image_url(v))
