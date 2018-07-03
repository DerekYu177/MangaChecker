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
import sys
import datetime

from dynamictableprint import DynamicTablePrint as dtp

from .retriever import Retriever
from .file_assistant import Assistant

DEFAULT_READING_FILE = 'reading_list.txt'

def _read_reading_list(args):
    """
    if the reading list is None we default
    else we check that the path exists
    then we read

    returns: dict of reading_list
    """

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

    return reading_list

def check(args):
    """
    we 'check' the reading file to know
    what the user is interested in, and provide
    the latest chapter for their benefit.

    This is the only public method in this class

    Returns: None
    """

    assistant = Assistant(args)

    reading_list = _read_reading_list(args)
    previously_read_manga = assistant.fetch_old_file()

    # gets us the most up to date manga
    # and the corresponding link that goes to it
    hound = Retriever(reading_list)
    new_manga = hound.search()

    updated_manga = assistant.compare(previously_read_manga, new_manga)

    # we compare the latest chapter to the records
    # and display if it is more recent
    dynamic_table = dtp(updated_manga, squish_column='title')
    dynamic_table.config.banner = 'Lastest Manga for {}'.format(datetime.date.today())
    dynamic_table.config.empty_banner = \
            'There is no new manga for you to read :('
    dynamic_table.write_to_screen()

    # we update the records
    assistant.update(updated_manga)

    return 0
