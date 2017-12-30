import argparse
import logging

DEBUG_HELP = 'Set debug mode'

logger = logging.getLogger('nowpass')
logger.setLevel(logging.DEBUG)


class Parser:
    def __init__(self):
        """Create the argument parser"""
        self._parser = argparse.ArgumentParser(description="nowpass command line password manager")
        self._subparsers = self._parser.add_subparsers(help='sub-command help', dest='command')

        self._create_add_parser()
        self._create_delete_parser()
        self._create_edit_parser()
        self._create_list_parser()
        self._create_search_parser()
        self._create_other_options()

    def _create_add_parser(self):
        add_parser = self._subparsers.add_parser('add', aliases=['a'], help='Add an Element (Website, Server etc.)')

        """Shortcuts"""
        add_parser.add_argument('-t', '--title', help='Title for the Element', default='', type=str)
        add_parser.add_argument('-u', '--url', help='URL for the login', default='', type=str)
        add_parser.add_argument('-p', '--password', help='Set the Password', default='', type=str)

    def _create_list_parser(self):
        list_parser = self._subparsers.add_parser('list', aliases=['l'], help='List Elements')
        list_parser.add_argument('-p', '--passwords', help='Including passwords', action="store_true")

        # TODO implement
        list_parser.add_argument('-t', '--today', help='Elements today', action="store_true")
        list_parser.add_argument('-j', '--json', help='Output as JSON string', action="store_true")

    def _create_search_parser(self):
        search_parser = self._subparsers.add_parser('search', aliases=['s'], help='Search for Elements')
        search_parser.add_argument('keyword', type=str, nargs='+',
                                   help='Title / URL etc. of the Element(s) to search for.')
        search_parser.add_argument('-t', '--type', help='Including passwords', default='', type=str)

    def _create_edit_parser(self):
        edit_parser = self._subparsers.add_parser('edit', aliases=['e'], help='Edit a element')
        edit_parser.add_argument('element_id', type=int, help='element to edit')

    def _create_delete_parser(self):
        delete_parser = self._subparsers.add_parser('delete', aliases=['del'], help='Delete a element')
        delete_parser.add_argument('element_ids', type=int, nargs='+', help='element(s) to delete')

    def _create_other_options(self):
        self._parser.add_argument("--debug", action="store_true",
                                  help=DEBUG_HELP)

        self._parser.add_argument("-f", "--logfile", default="~/nowpass-debug.log",
                                  help="Location of the debug log file")

    def get(self):
        return self._parser
