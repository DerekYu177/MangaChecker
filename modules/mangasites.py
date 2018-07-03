"""
Holds all of the classes where
each class represents on site that we support

Each class makes a request
"""

from urllib import request
from lxml import html
import re

import pandas as pd

class BaseMangaSite:
    """
    The base inheritable class of all Manga sites
    """

    MOST_RECENT = 4

    SITE = ''
    PATH = ''
    APPEND = ''

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

    def url(self, manga_site):
        """
        Finds the url based on the name of the manga provided
        """
        site = manga_site.manga.replace(' ', '_').lower()
        site = site.replace("!", '') # so far only Haikyuu! suffers from this
        full_link_to_site =     \
            manga_site.SITE   \
            + manga_site.PATH \
            + site              \
            + manga_site.APPEND

        print('looking for {} at {}'.format(site, full_link_to_site))
        return full_link_to_site

    def read(self):
        raise NotImplementedError

class DataFrameRow:
    """
    Represents a universal way of collecting all the data in one place
    guarentees that the frames will not be modified
    """
    REQUIRED = ["manga", "chapter", "title", "link"]
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

    @staticmethod
    def empty_manga_list():
        """
        Returns an empty dataframe with the columns initialized
        """
        return pd.DataFrame(columns=DataFrameRow.REQUIRED)

class ReadMs(BaseMangaSite):
    """
    Represents the readms site
    """

    SITE = 'https://readms.net'
    PATH = '/manga/'

    def read(self):
        """
        override the base class method
        """
        url = self.url(self)
        document = self.query(url)

        try:
            recent_releases = document\
                .xpath('//table[contains(@class, "table table-striped")]')[0]
        except IndexError: # nothing found
            print('{} is an invalid url'.format(url))
            return []

        dfs = []
        for index, dlink in enumerate(recent_releases.iterlinks()):
            if index > self.MOST_RECENT:
                break

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
    Represents manganelo
    """

    SITE = 'https://manganelo.com'
    PATH = '/manga/'
    APPEND = '_manga'

    def read(self):
        """
        override the base class method
        """
        url = self.url(self)
        document = self.query(url)

        try:
            recent_releases = document \
                .xpath('//div[contains(@class, "chapter-list")]')[0]
        except IndexError:
            return []

        dfs = []
        for index, dlink in enumerate(recent_releases.iterlinks()):
            if index > self.MOST_RECENT:
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
