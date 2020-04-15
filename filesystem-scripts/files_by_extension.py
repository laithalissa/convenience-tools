#!/usr/bin/env python
#
# Print how many of each file extension is found in the directory
# specified.
import argparse
import os

parser = argparse.ArgumentParser(
    description='Give a breakown of files by extension'
)

parser.add_argument(
    '-r',
    '--root',
    type=str,
    action='store',
    dest='root',
    required=True,
    help='The directory to scan through'
)

parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    dest='verbose'
)

if __name__ == '__main__':
    args = parser.parse_args()
    files_by_extension = {}
    for (dirpath, dirnames, filenames) in os.walk(args.root):
        for file in filenames:
            filename, file_extension = os.path.splitext(file)

            files = files_by_extension.get(file_extension, [])
            files.append(file)
            files_by_extension[file_extension] = files

    highest_count_width = len(str(reduce(
        lambda a, b: a if a > b else b,
        map(len, files_by_extension.values())
    )))

    longest_extension_width = reduce(
        lambda a, b: a if a > b else b,
        map(len, files_by_extension.keys())
    )

    if args.verbose:
        for (extension, files) in files_by_extension.iteritems():
            print '%s files:' % extension
            for file in files:
                print '  %s' % file

    for (extension, files) in sorted(
        files_by_extension.iteritems(),
        key=lambda t: len(t[1]),
        reverse=True
    ):
        print '%s %s files' % (
            str(len(files)).rjust(highest_count_width),
            extension.rjust(longest_extension_width)
        )
