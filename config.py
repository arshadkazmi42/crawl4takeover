global_config = {
    'debug': False,
    'directories': {
        'results': 'results'
    },
    'file_names': {
        'all_links': 'output.txt',
        'broken_links': 'broken.txt'
    },
    'regex': {
        'link': r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9]{1,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)'
    },
    'mime_types': {
        'media': ['audio', 'video', 'image', 'font', 'application/zip']
    },
    'tags': {
        'link': { 'a': 'href', 'link': 'href', 'script': 'src' },
        'image': {'img': 'src'}
    },
    'filters': {
        'enable': True,
        'tags': [ 'amazonaws.com', 'herokuapp.com', 'netlify.app', 'storage.googleapis.com', 'github.com', 'github.io', 'zendesk.com', 'bitbucket.org', 'fastly.net', 'readme.io', 'myshopify.com', 'surge.sh', 'mystrikingly.com']
    }
}