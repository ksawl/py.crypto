from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA384
from tpl.singletonMeta import SingletonMeta
from utils.file_crud import FileCRUD
from constant import *
import base64
import os


class SignCipher(metaclass=SingletonMeta):
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
    return "sign" + FileCRUD.new_key_filename(keylenght)

  def generate_key(self, block_size=2048):
    self.block_size = block_size
    key = RSA.generate(block_size)
    self._seckey = key
    self._pubkey = key.publickey()

  def check_keylenght(self, key):
    block_size = key.size_in_bits()
    for keylenght, size in SIGN_KEYLENGHT_DICT.items():
        if size == block_size:
          self.block_size = block_size
          self.keylenght = keylenght
          return True

  def save_pubkey(self, file_path):
    self.pubkey_filename = FileCRUD.write_file(file_path, self.key_public)

  def save_seckey(self, file_path):
    self.seckey_filename = FileCRUD.write_file(file_path, self.key_secret)

  def open_pubkey(self, file_path):
    key = FileCRUD.read_file(file_path)
    try:
      import_key = RSA.import_key(key)

      if(import_key.has_private() is False):
        self._pubkey = import_key
        self.pubkey_filename = FileCRUD.path_basename(file_path)
        self.check_keylenght(import_key)
        return True
      else:
        self.errormessage = ERROR_IS_NO_SIGN_PUBKEY
        return False

    except ValueError as err:
      self.errormessage = err
      return False

  def open_seckey(self, file_path):
    key = FileCRUD.read_file(file_path)
    try:
      import_key = RSA.import_key(key)

      if(import_key.has_private()):
        self._seckey = import_key
        self.seckey_filename = FileCRUD.path_basename(file_path)
        self.check_keylenght(import_key)
        return True
      else:
        self.errormessage = ERROR_IS_NO_SIGN_SECKEY
        return False

    except ValueError as err:
      self.errormessage = err
      return False

  def sign(self, data):
    if not self._seckey:
      self.errormessage = ERROR_NO_SIGN_SECKEY
      return False

    byte_data = base64.b64decode(data)
    signer = PKCS1_v1_5.new(self._seckey) 
    digest = SHA384.new() 
    digest.update(byte_data) 
    sign = signer.sign(digest) 
    return base64.b64encode(sign + byte_data)

  def verify_sign(self, signdata):
    if not self._pubkey:
      self.errormessage = ERROR_NO_SIGN_PUBKEY
      return False

    try:
      byte_signdata = base64.b64decode(signdata)
      signature = byte_signdata[:self._pubkey.size_in_bytes()]
      data = byte_signdata[self._pubkey.size_in_bytes():]

      signer = PKCS1_v1_5.new(self._pubkey) 
      digest = SHA384.new() 
      digest.update(data) 
      signer.verify(digest, signature)
      return base64.b64encode(data)

    except ValueError as err:
      self.errormessage = err
      return False
