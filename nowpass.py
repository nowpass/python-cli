#!/usr/bin/env python

import os
import sys
import logging
import nowpass.parser
import nowpass.element
import nowpass.engine
import nowpass.main_config
import errno

try:
    sys.setdefaultencoding('UTF8')
except Exception:
    pass

STORAGE_FOLDER = os.path.expanduser('~/.nowpass')
MAIN_CONFIG = STORAGE_FOLDER + '/main.conf'

# Testing work around for shortcuts
COMMANDS = {
    'del': 'delete', 'delete': 'delete',
    'a': 'add', 'add': 'add',
    'l': 'list', 'list': 'list',
    's': 'search', 'search': 'search',
    'e': 'edit', 'edit': 'edit'
}


def main():
    # Storage folder
    create_storage_folder(STORAGE_FOLDER)

    # Start args parser (needed for logging file)
    # Wrapper Class
    parser_class = nowpass.parser.Parser()
    parser = parser_class.get()

    args = parser.parse_args()

    # Logging
    logger = logging.getLogger('nowpass')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    # File logging with debug
    fh = logging.FileHandler(os.path.expanduser(args.logfile))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.debug('Starting nowpass CLI client')

    # Config
    main_config = nowpass.main_config.MainConfig(logger, MAIN_CONFIG)
    config = main_config.get_config()

    # Passphrase (stored or via input)
    if config['Encryption']['passphrase'] == '':
        config['Encryption']['passphrase'] = input('Enter your pass phrase: ')

    # Starting here we need a command
    if args.command is None:
        print('Please supply a command, check --help for more details.')
        exit(0)

    command = args.command

    logger.debug('Command: ' + command)

    # Get the Engine for processing tasks
    engine = nowpass.engine.Engine(logger, main_config)

    task_to_call = getattr(engine, COMMANDS[command])
    task_to_call(args)

    exit(0)


def create_storage_folder(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


if __name__ == "__main__":
    main()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
