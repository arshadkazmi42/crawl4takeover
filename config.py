global_config = {
    'debug': False,
    'directories': {
        'results': 'results'
    },
    'file_names': {
        'all_links': 'output.txt',
        'broken_links': 'broken.txt',
        'process': 'process.txt'
    },
    'regex': {
        'link': r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9]{1,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)'
    },
    'mime_types': {
        'media': ['audio', 'video', 'image', 'font', 'application/zip', 'application/x-debian-package', 'application/x-redhat-package-manager', 'application/x-apple-diskimage', 'application/x-msdos-program']
    },
    'tags': {
        'link': { 'a': 'href', 'link': 'href', 'script': 'src' },
        'image': {'img': 'src'}
    },
    'filters': {
        'enable': True,
        'tags': [ 'amazonaws.com', 'herokuapp.com', 'netlify.app', 'storage.googleapis.com', 'zendesk.com', 'bitbucket.org', 'fastly.net', 'readme.io', 'myshopify.com', 'surge.sh', 'mystrikingly.com']
    },
    'request': {
        'headers': {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    }
}
