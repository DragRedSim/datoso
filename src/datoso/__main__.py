"""Main entry point for datoso"""
import argparse
import logging
import os
import sys

from datoso import __version__
from datoso.commands.argparser import (
    add_all_seed_parser,
    add_config_parser,
    add_dat_parser,
    add_deduper_parser,
    add_doctor_parser,
    add_import_parser,
    add_log_parser,
    add_seed_parser,
)
from datoso.configuration import config
from datoso.configuration.logger import enable_logging, set_verbosity
from datoso.database.seeds.dat_rules import detect_first_run
from datoso.helpers import Bcolors

#---------Boilerplate to check python version ----------
if sys.version_info < (3, 10):  # noqa: UP036
    print('This is a Python 3 script. Please run it with Python 3.10 or above')
    sys.exit(1)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments

    Returns
    -------
        argparse.Namespace: An object to take the attributes.

    """
    #pylint: disable=too-many-locals,too-many-statements
    parser = argparse.ArgumentParser(description='Update dats from different sources.')
    subparser = parser.add_subparsers(help='sub-command help')

    parser.add_argument('-v', '--version', action='store_true', help='show version')
    parser.add_argument('-V', '--verbose', action='store_true', help='verbose output')

    add_log_parser(subparser)
    add_config_parser(subparser)
    add_doctor_parser(subparser)
    add_dat_parser(subparser)
    add_seed_parser(subparser)
    add_import_parser(subparser)
    add_deduper_parser(subparser)
    add_all_seed_parser(subparser)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    initial_setup(args)
    return args

def initial_setup(args) -> None:
    """Initial setup of datoso from command line arguments."""
    if getattr(args, 'version', False):
        print(__version__)
        sys.exit()
    if getattr(args, 'no_color', False) or os.name == 'nt':
        Bcolors.no_color()
    if getattr(args, 'quiet', False):
        set_verbosity(logging.WARNING)
        config['COMMAND']['Quiet'] = 'true'
    if getattr(args, 'verbose', False):
        set_verbosity(logging.DEBUG)
        config['COMMAND']['Verbose'] = 'true'
    if getattr(args, 'overwrite', False):
        config['PROCESS']['Overwrite'] = 'true'
    if getattr(args, 'logging', False):
        enable_logging()

def main():
    """Main function"""
    detect_first_run()
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
