import os
from nowpass.aes_cypher import AESCipher


class Password:
    CHARS = 'abcdefghijklmnopqrstuvwxyz'
    CHARS_UPPER = CHARS.upper()
    ALL_CHARS = CHARS + CHARS_UPPER
    NUMBERS = '0123456789'
    CHARS_NUMBERS = ALL_CHARS + NUMBERS
    SPECIAL = '!"§$&(/)=?@\'+-*#,.-_'
    CHARS_SPECIAL = ALL_CHARS + SPECIAL
    ALL = CHARS_NUMBERS + SPECIAL

    def __init__(self, logger, config, password='', crypt_password=''):
        self._logger = logger
        self._config = config
        self._password = password
        self._crypt_password = crypt_password
        self._is_encrypted = False
        self._handler = AESCipher(self._config['Encryption']['Passphrase'])

    def get_password(self):
        if self._password == '' and self._crypt_password != '':
            self._password = self._handler.decrypt(self._crypt_password)

        return self._password

    def set_password(self, password):
        self._password = password

    def get_crypted_password(self):
        if self._crypt_password != '':
            return self._crypt_password

        handler = AESCipher(self._config['Encryption']['Passphrase'])
        self._crypt_password = handler.encrypt(self._password)

        return self._crypt_password

    def gen_password(self, length=0):
        # Get length from config
        if length == 0:
            length = int(self._config['Generator']['Length'])

        gen_pw = ''

        chars = self.ALL_CHARS

        if self._config['Generator']['includeNumbers'] == 'y' and self._config['Generator']['includeSpecial'] == 'y':
            chars = self.ALL
        elif self._config['Generator']['includeNumbers'] == 'y':
            chars = self.CHARS_NUMBERS
        elif self._config['Generator']['includeSpecial'] == 'y':
            chars = self.CHARS_SPECIAL

        for x in range(0, length):
            gen_pw += chars[ord(os.urandom(1)) % len(chars)]

        self._password = gen_pw

        return self._password
