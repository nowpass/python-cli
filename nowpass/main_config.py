import configparser
import os


class MainConfig:
    def __init__(self, logger, path):
        self._logger = logger
        self._path = path
        self._config = {}

        if self.check_config_exists() is False:
            self.configure()

        self.load_config()

    def check_config_exists(self):
        return os.path.isfile(self._path)

    """First time configuration"""

    def configure(self):
        print('No configuration found for NOWPASS - First time setup')

        server_url = input('NOWPASS API server [http://localhost:1337] ') or 'http://localhost:1337'
        username = input('Username (Email): ')

        print('Next your API-Key is needed, you can find it in the settings of your user account on the API server.')

        api_key = input('API-Key: ')

        # Ask if they want to store the pass phrase
        passphrase = ''
        store_passphrase = input('Store your pass phrase (insecure)? (y/N) ') or 'N'

        if store_passphrase.lower() == 'y':
            print('Next we are going to set up your STRONG pass phrase, to encrypt and decrypt your passwords locally.')
            print('Note: The API server never receives unencrypted passwords, so when you loose it, you can\'t restore your passwords.')
            print('If you already stored passwords on the API server, please use your existing pass phrase.')

            passphrase = input('Pass phrase: ')

        config = configparser.RawConfigParser()
        config['API'] = {
            'url': server_url,
            'username': username,
            'api_key': api_key
        }

        config['Encryption'] = {
            'passphrase': passphrase,
            'store_passphrase': store_passphrase
        }

        config['Generator'] = {
            'length': 13,
            'include_numbers': 'y',
            'include_special': 'y'
        }

        # Store the result in the configfile
        with open(self._path, 'w') as configfile:
            config.write(configfile)

    def load_config(self):
        self._config = configparser.RawConfigParser()
        self._config.read(self._path)

    def get_config(self):
        return self._config

    def get(self, key, default=''):
        if self._config[key]:
            return self._config

        return default

    def store(self):
        with open(self._path, 'w') as configfile:
            self._config.write(configfile)
