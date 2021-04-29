import requests
from urllib import parse
import mimetypes


def is_image_url(url):    
    mimetype,encoding = mimetypes.guess_type(url)
    print(mimetype)
    return (mimetype and (mimetype.startswith('image') or mimetype.startswith('video')))


url='https://static-assets.mapbox.com/www/media-kit/mapbox_all-image-collections.zip'
v = parse.urlparse(url).path
print(v)
print(is_image_url(v))
