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
        print('nowpass main.cfg not found - First time setup')

        server_url = input('nowpass API server [http://localhost:1337] ') or 'http://localhost:1337'
        username = input('nowpass Username: ')
        password = input('nowpass Password: ')

        # Ask if they want to store the pass phrase
        passphrase = ''
        store_passphrase = input('Store your pass phrase (insecure)? (y/N) ') or 'N'

        if store_passphrase.lower() == 'y':
            print('Next we are going to set up your STRONG pass phrase, to encrypt and decrypt your passwords locally.')
            print('Note: The API server never receives unencrypted passwords, so when you loose it you can\'t restore your passwords.')
            print('If you already stored passwords on the API server, please use your existing pass phrase.')

            passphrase = input('nowpass pass phrase: ')

        config = configparser.RawConfigParser()
        config['API'] = {
            'Url': server_url,
            'Username': username,
            'Password': password
        }

        config['Encryption'] = {
            'Passphrase': passphrase,
            'StorePassphrase': store_passphrase
        }

        config['Cookie'] = {
            'sid': ''
        }

        config['Generator'] = {
            'Length': 12,
            'includeNumbers': 'y',
            'includeSpecial': 'y'
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
