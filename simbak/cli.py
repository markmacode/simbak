import argparse
import sys

import simbak


def parse_args(args):
    """Parses all the arguments sent through the command line.

    Returns:
        object: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog='simbak',
        description='Simple backup solution.',
    )
    parser.add_argument(
        '-s', '--source',
        type=str,
        nargs='+',
        help='The source(s) of the dir(s) you want to backup.',
        required=True,
    )
    parser.add_argument(
        '-d', '--destination',
        type=str,
        nargs='+',
        help='The backup destination(s) dir(s).',
        required=True,
    )
    parser.add_argument(
        '-n', '--name',
        type=str,
        help='The name of the backup.',
        required=True,
    )
    parser.add_argument(
        '-c', '--compression-level',
        type=int,
        default=6,
        help=('The compression level (1-9) of the gzip backup algorithm, '
              'default is 6.'),
    )
    return parser.parse_args(args)


def main():
    """Consider this the entry point to the command line utility."""
    args = parse_args(sys.argv[1:])
    simbak.backup(
        sources=args.source,
        destinations=args.destination,
        name=args.name,
        compression_level=args.compression_level)
