#!/usr/bin/env python
#
# Take all files within the specified directory, and if they match
# the provided regex, move them to the specified directory
#
# Example invocation:
# python flatten.py -p ".*.(avi|mp4)$" -s source -d destination --dry-run
import argparse
import errno
import os
import re
import shutil
import sys

parser = argparse.ArgumentParser(
    description=(
        'Take all files within the specified directory, and if they '
        'match the provided regex, move them to the specified directory'
    )
)

parser.add_argument(
    '-p',
    '--pattern',
    type=str,
    action='store',
    dest='pattern',
    required=True,
    help='File pattern to match'
)

parser.add_argument(
    '-s',
    '--source',
    type=str,
    action='store',
    dest='source',
    required=True,
    help='The directory to scan through'
)

parser.add_argument(
    '-d',
    '--destination',
    type=str,
    action='store',
    dest='destination',
    required=True,
    help=(
        'The default destination directory, creates it if it doesn\'t '
        'already exist'
    )
)

parser.add_argument(
    '-m',
    '--move',
    action='store_true',
    dest='move',
    help='Move instead of copy'
)

parser.add_argument(
    '--simple-names',
    action='store_true',
    dest='simple_names',
    help=(
        'Assume filename will be unique, if unset the script will join '
        'subdirectories with the filename to ensure there won\'t be any '
        'duplicates in the output'
    )
)

parser.add_argument(
    '--continue',
    action='store_true',
    dest='continue_',
    help='Skip duplicates in the destination directory, implies -f'
)

parser.add_argument(
    '-f',
    '--force',
    action='store_true',
    dest='force',
    help='Use the destination directory even if it exist and is non empty'
)

parser.add_argument(
    '--dry-run',
    action='store_true',
    dest='dry_run',
    help='Don\'t copy anything, just display what will be moved'
)


class Flattener:
    RESET_SEQ = '\033[0m'
    COLOUR_SEQ = '\033[1;%d'

    COLOURS = {
        'green': '\033[32m',
        'yellow': '\033[33m'
    }

    @staticmethod
    def status_tag(colour, message):
        return '[%s%s%s%s]' % (
            Flattener.COLOUR_SEQ,
            Flattener.COLOURS[colour],
            message,
            Flattener.RESET_SEQ
        )

    def __init__(
        self,
        pattern,
        source,
        destination,
        move,
        simple_names,
        force,
        dry_run,
        continue_
    ):
        self.pattern = re.compile(pattern)
        self.source = unicode(source, 'utf8')
        self.destination = unicode(destination, 'utf8')
        self.move = move
        self.simple_names = simple_names
        self.force = force
        self.dry_run = dry_run
        self.continue_ = continue_

        self.cwd = os.getcwd()
        self.handle_args()

        self.DRY_RUN_TAG = Flattener.status_tag('yellow', 'DRY_RUN')
        self.OK_TAG = Flattener.status_tag('green', 'OK')
        self.SKIPPED_TAG = Flattener.status_tag('yellow', 'SKIPPED')

    def handle_args(self):
        if not os.path.isdir(os.path.join(self.cwd, self.source)):
            print 'Source directory %s doesn\'t exist!'
            sys.exit(1)

        self.destination = os.path.join(
            self.cwd, self.destination or '%s-flattened' % self.source
        )

        if not self.dry_run:
            try:
                os.makedirs(self.destination)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
                elif (
                    not self.continue_ and os.listdir(self.destination)
                ):
                    raise Exception((
                        'Destination directory %s is not empty!'
                        % self.destination
                    ))

    def discover_files(self):
        """
        Search for files matching the given pattern and return a relocation
        plan (a dictionary of source string to destination string).
        """
        relocation_plan = {}
        for (dirpath, dirnames, filenames) in os.walk(self.source):
            for file in filenames:
                if not self.pattern.search(file):
                    continue

                destination_filename = (
                    file if self.simple_names else
                    '_'.join(os.path.split(dirpath)[1:] + (file,))

                )

                # Drop the root directory name, and join subsequent
                # directories with the filename to ensure unique names
                relocation_plan[os.path.join(dirpath, file)] = (
                    os.path.join(
                        self.destination,
                        destination_filename
                    )
                )

        return relocation_plan

    def move_files(self, relocation_plan):
        """
        Given a dictionary of source file strings to desitination file
        strings, move the files to the destination, if the continue option
        has been specified, the destination file's presence will be checked,
        and if it's found, no copy operation will be performed/

        @param relocation_plan a dictionary of source file to destination
                               file.
        """
        if self.dry_run:
            print 'Starting dry run...'
        else:
            print '%s %d files' % (
                'Moving' if self.move else 'Copying',
                len(relocation_plan)
            )

        for (source, destination) in relocation_plan.iteritems():
            if self.continue_ and os.path.exists(destination):
                print (
                    '%s already exists in the desitation directory %s' % (
                        source, self.SKIPPED_TAG
                    )
                ).encode(sys.stdout.encoding, errors='replace')
                continue

            # Handle printing utf to ascii console #WindowsSucks
            sys.stdout.write(
                ('%s -> %s' % (source, destination)).encode(
                    sys.stdout.encoding, errors='replace'
                )
            )
            sys.stdout.flush()

            if self.dry_run:
                print self.DRY_RUN_TAG
            else:
                try:
                    if self.move:
                        shutil.move(source, destination)
                    else:
                        shutil.copyfile(source, destination)
                except:
                    print 'Exception encountered processing %s' % source
                    raise
                print self.OK_TAG


def main(parser):
    args = parser.parse_args()

    f = Flattener(
        args.pattern,
        args.source,
        args.destination,
        args.move,
        args.simple_names,
        args.force,
        args.dry_run,
        args.continue_
    )
    relocation_plan = f.discover_files()
    f.move_files(relocation_plan)


if __name__ == '__main__':
    main(parser)
