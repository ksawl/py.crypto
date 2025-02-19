from tkinter import Tk
from tkinter import ttk
from view.frame_keys import FrameKeys
from view.frame_crypt import FrameCrypt
from constant import ROOT_TITLE, LABEL_KEYS_FRAME, LABEL_CRYPT_FRAME


class GuiDraw:
    def __init__(self):
        root = Tk()

        root.title(ROOT_TITLE)
        root.resizable(False, False)

        main_frame = ttk.Frame(root, padding=5)
        main_frame.grid(column=0, row=0, sticky="nsew")

        notebook = ttk.Notebook(main_frame)
        notebook.grid(column=0, row=0, sticky="nsew")

        tab_keys = ttk.Frame(notebook)
        tab_keys.grid(column=0, row=0, sticky="nsew")
        tab_crypt = ttk.Frame(notebook)
        tab_crypt.grid(column=0, row=0, sticky="nsew")

        notebook.add(tab_keys, text=LABEL_KEYS_FRAME, padding=10)
        notebook.add(tab_crypt, text=LABEL_CRYPT_FRAME, padding=10)

        FrameKeys(tab_keys)
        FrameCrypt(tab_crypt)

        root.mainloop()
