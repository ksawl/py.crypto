from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from tpl.singletonMeta import SingletonMeta
from utils.file_crud import FileCRUD
from constant import AES_KEYLENGHT_DICT, ERROR_NO_AES_KEY
import base64
import os


class AESCipher(metaclass=SingletonMeta):
    def __init__(self):
        self._key = ""
        self.filename = ""
        self.errormessage = ""

    @property
    def key(self):
        return base64.b64encode(self._key)

    @key.setter
    def key(self, value):
        self._key = base64.b64decode(value)

    def key_filename_generate(self, keylenght):
        return FileCRUD.new_key_filename(keylenght)

    def generate_key(self, block_size=16):
        self._key = get_random_bytes(block_size)
        return self.key

    def save_key(self, file_path):
        self.filename = FileCRUD.write_file(file_path, self._key)

    def open_key(self, file_path):
        file_info = os.stat(file_path)
        file_size = file_info.st_size

        if file_size not in list(AES_KEYLENGHT_DICT.values()):
            self.errormessage = ERROR_NO_AES_KEY
            return ("", "")

        for keylenght, size in AES_KEYLENGHT_DICT.items():
            if size == file_size:
                self.filename = FileCRUD.path_basename(file_path)
                self._key = FileCRUD.read_file(file_path)
                return (self.key, keylenght)

        return ("", "")

    def encrypt_CBC(self, plaintext):
        if self._key == "":
            self.errormessage = ERROR_NO_AES_KEY
            return False

        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        return base64.b64encode(iv + ciphertext)

    def decrypt_CBC(self, ciphertext):
        if self._key == "":
            self.errormessage = ERROR_NO_AES_KEY
            return False

        try:
            byte_ciphertext = base64.b64decode(ciphertext)
            iv = byte_ciphertext[: AES.block_size]
            byte_ciphertext = byte_ciphertext[AES.block_size :]

            cipher = AES.new(self._key, AES.MODE_CBC, iv)
            decrypt = cipher.decrypt(byte_ciphertext)
            return unpad(decrypt, AES.block_size)

        except OSError as err:
            self.errormessage = err
            return False
        except ValueError as err:
            self.errormessage = err
            return False
