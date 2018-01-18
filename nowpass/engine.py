import requests
from terminaltables import SingleTable
from nowpass.password import Password
from nowpass.aes_cypher import AESCipher


class Engine:
    # API Version
    VERSION = 'v1'

    # API Endpoints (TODO move to own class)
    GET_ELEMENTS = '/api/' + VERSION + '/elements'
    GET_ELEMENT = '/api/' + VERSION + '/elements/'

    POST_ELEMENT = '/api/' + VERSION + '/elements'

    # Login
    PUT_LOGIN = '/api/' + VERSION + '/entrance/login'

    # Kinds of elements
    KINDS = ['website', 'mail', 'router', 'server', 'mail']

    """
    Logger
    """

    def __init__(self, logger, main_config):
        self._logger = logger
        self._main_config = main_config
        self._config = main_config.get_config()
        self._headers = {'api-key': self._config['API']['api_key']}

    """
    Add an Element (TODO move input to own logic)
    """

    def add(self, args):
        print('Kind of Element you want to add:')

        for idx, kind in enumerate(self.KINDS):
            print(str(idx) + ')', kind.capitalize())

        kind = self.KINDS[int(input('Enter number [0]: ') or '0')]
        title = input('Title: ') or 'Untitled'
        url = input('URL (optional): ') or ''
        username = input('Username (optional): ') or ''
        generate_pass = input('Generate password (Y/n) ') or 'y'

        password_obj = Password(self._logger, self._config)

        if generate_pass.lower() == 'y':
            input_password = password_obj.gen_password()
            print('Generated Password:', input_password)
        else:
            input_password = input('Password (optional): ') or ''
            password_obj.set_password(input_password)

        comment = input('Comment (optional): ') or ''

        # Not provided / default values
        form_data = ''
        status = 1

        # We need to crypt the password
        crypted_password = password_obj.get_crypted_password()

        # Just to not use it again
        del input_password

        payload = {
            'kind': kind,
            'title': title,
            'url': url,
            'username': username,
            'password': crypted_password,
            'form_data': form_data,
            'comment': comment,
            'status': status,
            'source': 'cli'
        }

        self._post_element(payload)

    """
    Get the List items (TODO optimize)
    """

    def list(self, args):
        get_url = self._config['API']['url'] + self.GET_ELEMENTS

        self._request_elements(args, get_url, args.passwords)

    def search(self, args):
        search_word = ' '.join(args.keyword)

        self._logger.debug('Searching for ' + str(search_word))

        get_url = self._config['API']['url'] + self.GET_ELEMENTS
        get_url += '?title=' + search_word + '&url=' + search_word + '&comment=' + search_word

        self._request_elements(args, get_url, True)

    def edit(self, args):
        print('TODO')

    def delete(self, args):
        print('TODO')

    def _request_elements(self, args, get_url, show_passwords=False):
        r = requests.get(get_url, headers=self._headers)

        if r.status_code != 200:
            raise Exception('Failed to retrieve Elements (Status ' + str(r.status_code) + ')\nError: ' + r.text)

        elements = r.json()['elements']

        if len(elements) == 0:
            print('No Elements found.')
            return

        data = []
        password_header = ''

        if show_passwords:
            password_header = 'Password'

        data.append(['Title', 'URL', 'Username', password_header, 'Type'])

        # We only need the handler when we show passwords
        handler = False

        if show_passwords:
            handler = AESCipher(self._config['Encryption']['Passphrase'])

        for element in elements:
            password = ''

            if show_passwords and element['password'] != '':
                try:
                    password = handler.decrypt(element['password'])
                except:
                    pass

            kind = str(element['kind']).capitalize()

            data.append([element['title'], element['url'], element['username'], password, kind])

        table = SingleTable(data)
        print(table.table)

    """
    Store an Element to the API (TODO outsource)
    """

    def _post_element(self, payload):
        self._logger.debug('Saving new Element at ' + self._config['API']['url'] + self.POST_ELEMENT)

        r = requests.post(self._config['API']['url'] + self.POST_ELEMENT, json=payload, headers=self._headers)

        if r.status_code != 200:
            raise Exception('Failed to save Element (Status ' + str(r.status_code) + ')\nError: ' + r.text)

        element = r.json()['element']

        print('Created ' + str(element['kind']).capitalize() + ' with id ' + str(element['id']))
