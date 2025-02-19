from tkinter import ttk, VERTICAL
from view.frame_encrypt import FrameEncrypt
from view.frame_decrypt import FrameDecrypt
from constant import LABEL_METHOD_FRAME, LABEL_ENCRYPT_FRAME, LABEL_DECRYPT_FRAME


class FrameCrypt:
    def __init__(self, master):
        self.frame_draw(master)

    def frame_draw(self, master):
        """Start Paned"""
        paned = ttk.Panedwindow(master, orient=VERTICAL)
        paned.grid(row=0, column=0, sticky="nsew")

        """ Method Frame """
        method_labelframe = ttk.Labelframe(paned, text=LABEL_METHOD_FRAME, padding=10)
        method_labelframe.grid(row=0, column=0, sticky="nsew")

        # crypt_method = FrameMethod(method_labelframe)

        """ Tabs """
        notebook = ttk.Notebook(paned)
        notebook.grid(column=0, row=0, sticky="nsew")

        tab_encrypt = ttk.Frame(notebook)
        tab_encrypt.grid(column=0, row=0, sticky="nsew")
        tab_decrypt = ttk.Frame(notebook)
        tab_decrypt.grid(column=0, row=0, sticky="nsew")

        notebook.add(tab_encrypt, text=LABEL_ENCRYPT_FRAME, padding=10)
        notebook.add(tab_decrypt, text=LABEL_DECRYPT_FRAME, padding=10)

        FrameEncrypt(tab_encrypt)
        FrameDecrypt(tab_decrypt)

        """ End Paned """
        paned.add(method_labelframe)
        paned.add(notebook)
