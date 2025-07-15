KEYS_DIR = "keys"
ENCRYPT_DIR = "encrypt"
DECRYPT_DIR = "decrypt"
METHODS_LIST = ["AES", "RSA", "AES+RSA"]
AES_MODES_LIST = ["CBC", "OFB", "CFB"]
AES_KEYLENGHT_DICT = {"AES-128": 16, "AES-192": 24, "AES-256": 32}
RSA_KEYLENGHT_DICT = {
    "RSA-1536": 1536,
    "RSA-2048": 2048,
    "RSA-3072": 3072,
    "RSA-4096": 4096,
}
SIGN_KEYLENGHT_DICT = {
    "RSA-1536": 1536,
    "RSA-2048": 2048,
    "RSA-3072": 3072,
    "RSA-4096": 4096,
}

ROOT_TITLE = "Encryption and decryption tool"
LABEL_METHOD_FRAME = "Choose a method"
LABEL_KEYS_FRAME = "Keys"
LABEL_CRYPT_FRAME = "Encrypt / Decrypt"
LABEL_ENCRYPT_FRAME = "Encrypt"
LABEL_DECRYPT_FRAME = "Decrypt"
LABEL_KEY_AES_FRAME = "AES key"
LABEL_KEY_AES_INIT = "<<< Create or open an AES key"
LABEL_KEY_AES_NEEDSAVE = "AES key must be saved >>>"
LABEL_KEY_RSA_FRAME = "RSA keys"
LABEL_PUBKEY_RSA_NEEDSAVE = "RSA public key must be saved >>>"
LABEL_SECKEY_RSA_NEEDSAVE = "You must save the RSA private key >>>"
LABEL_PUBKEY_RSA_INIT = "<<< Create or open an RSA public key"
LABEL_SECKEY_RSA_INIT = "<<< Generate or open a private RSA key"
LABEL_KEY_SIGN_FRAME = "Signature keys"
LABEL_PUBKEY_SIGN_NEEDSAVE = "The public signing key must be saved. >>>"
LABEL_SECKEY_SIGN_NEEDSAVE = "It is necessary to save the private signing key >>>"
LABEL_PUBKEY_SIGN_INIT = "<<< Create or open a public signing key"
LABEL_SECKEY_SIGN_INIT = "<<< Create or open a private signing key"
LABEL_SIGN_CHECK = "Sign"
LABEL_FROM_TEXT_RADIO = "Text encryption"
LABEL_FROM_FILE_RADIO = "File encryption"

BTN_GENERATE_KEY = "Generate"
BTN_SHOW_KEY = "Show"
BTN_OPEN_KEY = "Open"
BTN_SAVE_KEY = "Save"
BTN_ENCRYPT = "Encrypt"
BTN_DECRYPT = "Decrypt"

TITLE_ERROR_MESSAGE = "Error"
ERROR_UNKNOWN = "Unknown error"
ERROR_IS_NO_RSA_PUBKEY = "This file does not contain an RSA public key.."
ERROR_IS_NO_RSA_SECKEY = "This file does not contain an RSA private key.."
ERROR_IS_NO_SIGN_PUBKEY = "This file does not contain a public signing key.."
ERROR_IS_NO_SIGN_SECKEY = "This file does not contain a private signing key.."
ERROR_IS_NO_TEXT = "Enter text"
ERROR_IS_NO_FILE = "Select file"
ERROR_NO_AES_KEY = "AES key not found"
ERROR_NO_RSA_PUBKEY = "RSA public key not found"
ERROR_NO_RSA_SECKEY = "RSA private key not found"
ERROR_NO_SIGN_PUBKEY = "Public signing key not found"
ERROR_NO_SIGN_SECKEY = "Private signing key not found"
ERROR_DECODE = "Decoding error"

TITLE_INFO_MESSAGE = "Information"
INFO_COPY_CLIPBOARD_OK = "Text copied to clipboard."
