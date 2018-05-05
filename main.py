from modules import checker
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default='reading_file.txt', help='insert here the custom .txt file of the reading list')
    args = parser.parse_args()
    checker.check(args)
