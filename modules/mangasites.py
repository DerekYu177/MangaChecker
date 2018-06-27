"""
Holds all of the classes where
each class represents on site that we support

Each class makes a request
"""

import pandas as pd

from urllib import request
from lxml import html

class BaseMangaSite:
    """
    The base inheritable class of all Manga sites
    """

    def __init__(self, manga):
        self.manga = manga

    @staticmethod
    def __identify(url):
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
                     "(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        headers = {'User-Agent': user_agent}
        return request.Request(url, b'', headers)

    def query(self, url):
        """
        Makes the query to the site.
        We assume that sites will try to block robots
        we self identify, since we're not going to scrape images
        """

        req = self.__identify(url)
        root_html = request.urlopen(req).read()
        return html.document_fromstring(root_html)

    @staticmethod
    def url(manga_site):
        """
        Finds the url based on the name of the manga provided
        """
        return manga_site.SITE + manga_site.PATH + manga_site.manga.replace(' ', '_').lower()

class DataFrameRow:
    """
    Represents a universal way of collecting all the data in one place
    guarentees that the frames will not be modified
    """
    REQUIRED = ["chapter", "title", "link", "manga"]
    __slots__ = [*REQUIRED, "dataframe"]

    def __init__(self, chapter_number=0, chapter_title=None, chapter_link=None,
                 manga=None):
        self.chapter = chapter_number
        self.title = chapter_title
        self.link = chapter_link
        self.manga = manga

        chapter_links = dict((c_name, [getattr(self, c_name)]) for c_name in
                            self.REQUIRED)
        self.dataframe = pd.DataFrame(chapter_links, columns=self.REQUIRED)

class ReadMs(BaseMangaSite):
    """
    Represents the readms site
    """

    SITE = 'https://readms.net'
    PATH = '/manga/'

    def read(self):
        url = self.url(self)
        document = self.query(url)

        recent_releases = document\
            .xpath('//table[contains(@class, "table table-striped")]')[0]

        dfs = []
        for dlink in recent_releases.iterlinks():
            element, _, rel_link, _ = dlink

            # get the first occurance
            ch_number, ch_title = element.text.split(' - ', 1)

            ch_link = self.SITE + rel_link

            df = DataFrameRow(
                chapter_number=ch_number,
                chapter_title=ch_title,
                chapter_link=ch_link,
                manga=self.manga,
            )

            dfs.append(df)

        return dfs

class Manganelo(BaseMangaSite):
    """
    Represents mangafox
    """

    SITE = 'https://manganelo.com'
    PATH = '/manga/'

    LAST_RECENT = 4

    def read(self):
        """
        We only get the last four, to keep in line with MangaStream
        """
        url = self.url(self) + '_manga'
        document = self.query(url)
        recent_releases = document \
            .xpath('//div[contains(@class, "chapter-list")]')[0]

        dfs = []
        for index, dlink in enumerate(recent_releases.iterlinks()):
            if index > self.LAST_RECENT:
                break

            element, _, ch_link, _ = dlink

            # sometimes you won't find a title, manganelo doesn't do titles
            if ":" not in element.text:
                ch_number, ch_title = element.text, None
            else:
                ch_number, ch_title = element.text.split(':', 1)
                ch_number = ch_number.replace('Chapter', '').strip()

            df = DataFrameRow(
                chapter_number=ch_number,
                chapter_title=ch_title,
                chapter_link=ch_link,
                manga=self.manga,
            )

            dfs.append(df)

        return dfs
