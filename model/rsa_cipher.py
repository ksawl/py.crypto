from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from tpl.singletonMeta import SingletonMeta
from utils.file_crud import FileCRUD
from constant import (
    RSA_KEYLENGHT_DICT,
    ERROR_IS_NO_RSA_PUBKEY,
    ERROR_IS_NO_RSA_SECKEY,
    ERROR_NO_RSA_PUBKEY,
    ERROR_NO_RSA_SECKEY,
)
import base64


class RSACipher(metaclass=SingletonMeta):
    def __init__(self):
        self._pubkey = ""
        self._seckey = ""
        self.pubkey_filename = ""
        self.seckey_filename = ""
        self.block_size = None
        self.keylenght = None
        self.errormessage = ""

    @property
    def key_public(self):
        return self._pubkey.export_key("PEM")

    @property
    def key_secret(self):
        return self._seckey.export_key("PEM")

    def key_filename_generate(self, keylenght):
        return FileCRUD.new_key_filename(keylenght)

    def generate_key(self, block_size=2048):
        key = RSA.generate(block_size)
        self.block_size = block_size
        self._seckey = key
        self._pubkey = key.publickey()

    def check_keylenght(self, key):
        block_size = key.size_in_bits()
        for keylenght, size in RSA_KEYLENGHT_DICT.items():
            if size == block_size:
                self.block_size = block_size
                self.keylenght = keylenght
                return True

        return False

    def save_pubkey(self, file_path):
        self.pubkey_filename = FileCRUD.write_file(file_path, self.key_public)

    def save_seckey(self, file_path):
        self.seckey_filename = FileCRUD.write_file(file_path, self.key_secret)

    def open_pubkey(self, file_path):
        key = FileCRUD.read_file(file_path)
        try:
            import_key = RSA.import_key(key)
            check_key = self.check_keylenght(import_key)

            if not check_key or import_key.has_private() is not False:
                self.errormessage = ERROR_IS_NO_RSA_PUBKEY
                return False

            self._pubkey = import_key
            self.pubkey_filename = FileCRUD.path_basename(file_path)
            return True

        except ValueError as err:
            self.errormessage = err
            return False

    def open_seckey(self, file_path):
        key = FileCRUD.read_file(file_path)
        try:
            import_key = RSA.import_key(key)
            check_key = self.check_keylenght(import_key)

            if not check_key or not import_key.has_private():
                self.errormessage = ERROR_IS_NO_RSA_SECKEY
                return False

            self._seckey = import_key
            self.seckey_filename = FileCRUD.path_basename(file_path)
            return True

        except ValueError as err:
            self.errormessage = err
            return False

    def encrypt(self, plaintext):
        if not self._pubkey:
            self.errormessage = ERROR_NO_RSA_PUBKEY
            return False

        try:
            cipher = PKCS1_OAEP.new(self._pubkey)
            ciphertext = cipher.encrypt(plaintext)
            return base64.b64encode(ciphertext)

        except ValueError as err:
            self.errormessage = err
            return False

    def decrypt(self, ciphertext):
        if not self._seckey:
            self.errormessage = ERROR_NO_RSA_SECKEY
            return False

        try:
            ciphertext = base64.b64decode(ciphertext)
            cipher = PKCS1_OAEP.new(self._seckey)
            plaintext = cipher.decrypt(ciphertext)
            return plaintext

        except ValueError as err:
            self.errormessage = err
            return False

    def split_encrypted_data(self, ciphertext):
        if not self._seckey:
            self.errormessage = ERROR_NO_RSA_SECKEY
            return False

        try:
            key_bytes = self._seckey.size_in_bytes()
            key, text = FileCRUD.split_byte_strings(ciphertext, key_bytes)
            return key, text

        except ValueError as err:
            self.errormessage = err
            return False
