"""
We read from the reading file supplied either by the user
or the default reading_list.txt

We check each entry in this file, the name of the manga and
the site that the user prefers, and finds the most up-to-date chapter
and presents it to the user

We assume that the user is already caught up and will only be
interested in the latest chapter

We will update the records to reflect this change
"""

import os
from .retriever import Retriever
from .filereader import Updater

DEFAULT_READING_FILE = 'reading_list.txt'

def check(args):
    """
    we 'check' the reading file to know
    what the user is interested in, and provide
    the latest chapter for their benefit.

    This is the only public method in this class

    Returns: None
    """
    # if the reading list is None we default
    # else we check that the path exists
    # then we read

    reading_file = DEFAULT_READING_FILE if args.file is None else args.file

    if not os.path.isfile(reading_file):
        return OSError

    reading_list = {}
    with open(reading_file, 'r') as file:
        for line in file:
            line = line.rstrip()
            try:
                key, val = line.split(':')
                reading_list[key] = val
            except ValueError:
                print('One of your mangas is missing a site')
                reading_list[line] = None

    # gets us the most up to date manga
    # and the corresponding link that goes to it
    hound = Retriever(reading_list)
    updated_manga = hound.search()

    # we compare the latest chapter to the records
    # and display if it is more recent
    _display_latest_manga(updated_manga)

    # we update the records
    Updater(updated_manga).update()

    return 0

def _display_latest_manga(latest_manga):
    """
    latest_manga should be a DataFrame
    | Manga | Chapter Title | Chapter Number | Chapter Link (alap) | Updated |

    reads the latest manga against the records
    and displays the changes accordingly

    Returns: None
    """

    return latest_manga
