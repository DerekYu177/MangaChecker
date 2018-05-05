from urllib import request
from lxml import html

import pandas as pd

def __identify(url):
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
                 "(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    headers = {'User-Agent': user_agent}
    return request.Request(url, b'', headers)

def readms(manga):
    site = 'https://readms.net'
    path = '/manga/'
    url = site + path + manga.replace(' ', '_').lower()

    # site is protected and will throw a 403
    # if we try to access it
    # we aren't trying to scrape the actual images
    # so it'll be ok
    req = __identify(url)
    root_html = request.urlopen(req).read()
    document = html.document_fromstring(root_html)

    recent_releases = document\
            .xpath('//table[contains(@class, "table table-striped")]')[0]

    chapter_links = {
        "manga": [],
        "chapter_number" : [],
        "chapter_title": [],
        "chapter_link": [],
    }

    for dlink in recent_releases.iterlinks():
        element, _, rel_link, _ = dlink
        ch_number, ch_title = element.text.split(' - ')
        ch_link = site + rel_link

        chapter_links["chapter_number"].append(ch_number)
        chapter_links["chapter_title"].append(ch_title)
        chapter_links["chapter_link"].append(ch_link)
        chapter_links["manga"].append(manga)

    return pd.DataFrame(chapter_links)

SUPPORTED_SITES = {
    'Manga Stream': readms,
    'ReadMS' : readms
}

def _retrieve(manga, site):
    if not site in SUPPORTED_SITES.keys():
        raise NotImplementedError

    reader = SUPPORTED_SITES[site]

    # TODO: we should be finding only the most recent
    # chapter to show, unless we keep track of which chapter the user is
    # currently on...

    return reader(manga)

class Retriever(object):
    def __init__(self, manga_list):
        self.manga_list = manga_list
        self.data_frame = None

    def search(self):
        mangas = [_retrieve(manga, site) for manga, site in self.manga_list.items()]
        all_mangas = pd.concat(mangas)
        return all_mangas
