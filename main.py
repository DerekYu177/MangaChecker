"""
The interface for the user to interact with this CLI
Provided an optional reading_file.txt, we search each file on a newline
together with the preferred source
and provide a reading list of updated chapters
"""
import argparse
import sys

from modules import checker

# create the db locally, easier to delete
DB = 'db.csv'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file', default='reading_file.txt',
        help='insert here the custom .txt file of the reading list')
    parser.add_argument(
        '-d', '--database', default=DB,
        help='relative location of where you would like to store data \
              associated with previously read manga')
    parser.add_argument(
        '-c', '--clear', action='store_true',
        help='clears the DB prior to search')
    args = parser.parse_args()
    checker.check(args)
