from tkinter import ttk, VERTICAL
from view.frame_key_aes import FrameKeyAES
from view.frame_key_rsa import FrameKeyRSA
from view.frame_key_sign import FrameKeySign
from constant import LABEL_KEY_AES_FRAME, LABEL_KEY_RSA_FRAME, LABEL_KEY_SIGN_FRAME


class FrameKeys:
    def __init__(self, master):
        self.frame_draw(master)

    """ Keys Frame """

    def frame_draw(self, master):
        paned = ttk.Panedwindow(master, orient=VERTICAL)
        paned.grid(row=0, column=0, sticky="nsew")

        """ AES Frame """
        key_aes_labelframe = ttk.Labelframe(paned, text=LABEL_KEY_AES_FRAME, padding=5)
        key_aes_labelframe.grid(row=0, column=0, sticky="nsew")

        FrameKeyAES(key_aes_labelframe)

        """ RSA Frame """
        key_rsa_labelframe = ttk.Labelframe(paned, text=LABEL_KEY_RSA_FRAME, padding=5)
        key_rsa_labelframe.grid(row=1, column=0, sticky="nsew")

        FrameKeyRSA(key_rsa_labelframe)

        """ Sign Frame """
        key_sign_labelframe = ttk.Labelframe(
            paned, text=LABEL_KEY_SIGN_FRAME, padding=5
        )
        key_sign_labelframe.grid(row=2, column=0, sticky="nsew")

        FrameKeySign(key_sign_labelframe)

        paned.add(key_aes_labelframe)
        paned.add(key_rsa_labelframe)
        paned.add(key_sign_labelframe)
