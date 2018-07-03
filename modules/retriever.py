"""
Coordinates finding all of the mangas
"""
import itertools
import pandas as pd

from .mangasites import ReadMs, Manganelo

SUPPORTED_SITES = {
    'Manga Stream': ReadMs,
    'ReadMS' : ReadMs,
    'Manganelo': Manganelo,
}

def _retrieve(manga, site):
    if not site in SUPPORTED_SITES.keys():
        raise NotImplementedError

    manga_klass = SUPPORTED_SITES[site]

    return manga_klass(manga).read()

class Retriever(object):
    def __init__(self, manga_list):
        self.manga_list = manga_list
        self.data_frame = None

    def search(self):
        """
        searches from the mangalist
        returns a single DataFrame
        """
        mangas = [_retrieve(manga, site) for manga, site in self.manga_list.items()]
        mangas = list(itertools.chain.from_iterable(mangas))
        mangas_as_dataframes = [manga.dataframe for manga in mangas]

        all_mangas = pd.concat(mangas_as_dataframes, ignore_index=True)
        return all_mangas
