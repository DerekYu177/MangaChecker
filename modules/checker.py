import os

DEFAULT_READING_FILE = 'reading_list.txt'

def check(args):
    # if the reading list is None we default
    # else we check that the path exists
    # then we read

    reading_file = DEFAULT_READING_FILE if args.file is None else args.file

    if not os.path.isfile(reading_file):
        return OSError

    reading_list = []
    with open(reading_file, 'r') as f:
        reading_list = [name.rstrip() for name in f]

    import pdb; pdb.set_trace()
    return 0
