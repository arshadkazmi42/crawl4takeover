import requests
from urllib import parse
import mimetypes


def is_image_url(url):    
    mimetype,encoding = mimetypes.guess_type(url)
    return (mimetype and (mimetype.startswith('image') or mimetype.startswith('video')))


v = parse.urlparse('http://video.branch.io/64968558/68466727/66ccc7bb55115becf719e373b887792b/video_medium/tus-usuarios-de-app-son-mas-video.mp4?source=podcast').path
print(v)
print(is_image_url(v))
