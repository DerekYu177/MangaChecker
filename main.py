"""
The interface for the user to interact with this CLI
Provided an optional reading_file.txt, we search each file on a newline
together with the preferred source
and provide a reading list of updated chapters
"""
import argparse
import sys

from modules import checker

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file', default='reading_file.txt',
        help='insert here the custom .txt file of the reading list')
    args = parser.parse_args()
    checker.check(args)
