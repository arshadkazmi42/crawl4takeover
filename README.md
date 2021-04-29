# crawl4takeover
Crawler to crawl all the external links from a website

## Setup

```bash
$ pip install -r requirements.txt
```

## Usage

```bash
$ python scan.py {URL}
```

## Working

1. Script scans the page and get all the URLs from the page and corresponding JS files
2. Stores the same domain links in memory to scan further
3. It filters only selected links as configured in `scan.py`
4. Script creates two output files
   - `output.txt`: It contains all the links which are found after filter
   - `broken.txt`: It contains all the links which are broken from the above list
