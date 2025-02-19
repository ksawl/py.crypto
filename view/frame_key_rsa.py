from tkinter import ttk, filedialog, messagebox, StringVar
from model.rsa_cipher import RSACipher
from view.components.message_dialog import MessageDialog
from constant import (
    KEYS_DIR,
    LABEL_PUBKEY_RSA_INIT,
    LABEL_SECKEY_RSA_INIT,
    RSA_KEYLENGHT_DICT,
    BTN_SHOW_KEY,
    BTN_OPEN_KEY,
    BTN_SAVE_KEY,
    BTN_GENERATE_KEY,
    LABEL_PUBKEY_RSA_NEEDSAVE,
    LABEL_SECKEY_RSA_NEEDSAVE,
    TITLE_ERROR_MESSAGE,
)


class FrameKeyRSA:
    def __init__(self, master):
        self.cipher = RSACipher()

        self.pubkey = StringVar()
        self.seckey = StringVar()
        self.pubkey_fname = StringVar(value=LABEL_PUBKEY_RSA_INIT)
        self.seckey_fname = StringVar(value=LABEL_SECKEY_RSA_INIT)
        self.keylenght = StringVar()

        self.frame_draw(master)

    def frame_draw(self, master):
        master.columnconfigure(3, weight=1)

        combo = ttk.Combobox(
            master,
            width=10,
            values=list(RSA_KEYLENGHT_DICT.keys()),
            textvariable=self.keylenght,
            state="readonly",
        )
        combo.current(0)
        combo.grid(row=0, column=0, sticky="we", pady=[0, 5])

        self.pubkey_btn_show = ttk.Button(
            master, text=BTN_SHOW_KEY, command=self.pubkey_show, state=["disabled"]
        )
        self.pubkey_btn_show.grid(row=0, column=1, sticky="e", pady=[0, 5], padx=[5, 0])

        ttk.Button(master, text=BTN_OPEN_KEY, command=self.pubkey_open).grid(
            row=0, column=2, sticky="e", pady=[0, 5], padx=[5, 0]
        )

        entry_pubkey_fname = ttk.Entry(
            master, width=20, textvariable=self.pubkey_fname, state="readonly"
        )
        entry_pubkey_fname.grid(row=0, column=3, sticky="we", pady=[0, 5], padx=[5, 0])

        self.pubkey_btn_save = ttk.Button(
            master, text=BTN_SAVE_KEY, command=self.pubkey_save, state=["disabled"]
        )
        self.pubkey_btn_save.grid(row=0, column=4, sticky="e", pady=[0, 5], padx=[5, 0])

        ttk.Button(
            master, width=11, text=BTN_GENERATE_KEY, command=self.key_generate
        ).grid(row=1, column=0, sticky="we")

        self.seckey_btn_show = ttk.Button(
            master, text=BTN_SHOW_KEY, command=self.seckey_show, state=["disabled"]
        )
        self.seckey_btn_show.grid(row=1, column=1, sticky="e", padx=[5, 0])

        ttk.Button(master, text=BTN_OPEN_KEY, command=self.seckey_open).grid(
            row=1, column=2, sticky="e", padx=[5, 0]
        )

        entry_seckey_fname = ttk.Entry(
            master, width=20, textvariable=self.seckey_fname, state="readonly"
        )
        entry_seckey_fname.grid(row=1, column=3, sticky="we", padx=[5, 0])

        self.seckey_btn_save = ttk.Button(
            master, text=BTN_SAVE_KEY, command=self.seckey_save, state=["disabled"]
        )
        self.seckey_btn_save.grid(row=1, column=4, sticky="e", padx=[5, 0])

    """ Comands """

    def key_generate(self, *args):
        block_size = RSA_KEYLENGHT_DICT[self.keylenght.get()]
        self.cipher.generate_key(block_size=block_size)
        self.pubkey.set(self.cipher.key_public.decode(encoding="utf-8"))
        self.seckey.set(self.cipher.key_secret.decode(encoding="utf-8"))

        self.pubkey_fname.set(LABEL_PUBKEY_RSA_NEEDSAVE)
        self.seckey_fname.set(LABEL_SECKEY_RSA_NEEDSAVE)
        self.pubkey_btn_show.state(["!disabled"])
        self.pubkey_btn_save.state(["!disabled"])
        self.seckey_btn_show.state(["!disabled"])
        self.seckey_btn_save.state(["!disabled"])

    def pubkey_save(self, *args):
        if self.cipher.key_public == "":
            return False

        keylenght = "receiver-" + self.keylenght.get()
        filename = self.cipher.key_filename_generate(keylenght=keylenght)
        file_path = filedialog.asksaveasfile(
            defaultextension=".pem",
            filetypes=[("Key types", ".pem")],
            initialdir=KEYS_DIR,
            initialfile=filename,
        )
        if file_path is None or file_path.name == "":
            return False

        self.cipher.save_pubkey(file_path=file_path.name)
        self.pubkey_fname.set(self.cipher.pubkey_filename)
        self.pubkey_btn_save.state(["disabled"])

    def seckey_save(self, *args):
        if self.cipher.key_secret == "":
            return False

        keylenght = "private-" + self.keylenght.get()
        filename = self.cipher.key_filename_generate(keylenght=keylenght)
        file_path = filedialog.asksaveasfile(
            defaultextension=".pem",
            filetypes=[("Key types", ".pem")],
            initialdir=KEYS_DIR,
            initialfile=filename,
        )
        if file_path is None or file_path.name == "":
            return False

        self.cipher.save_seckey(file_path=file_path.name)
        self.seckey_fname.set(self.cipher.seckey_filename)
        self.seckey_btn_save.state(["disabled"])

    def pubkey_open(self, *args):
        file_path = filedialog.askopenfile(
            defaultextension=".pem",
            filetypes=[("Key types", ".pem")],
            initialdir=KEYS_DIR,
        )
        if file_path is None or file_path.name == "":
            return False

        if not self.cipher.open_pubkey(file_path.name):
            messagebox.showerror(
                title=TITLE_ERROR_MESSAGE, message=self.cipher.errormessage
            )
            return False

        self.keylenght.set(self.cipher.keylenght)
        self.pubkey.set(self.cipher.key_public.decode(encoding="utf-8"))
        self.pubkey_fname.set(self.cipher.pubkey_filename)
        self.pubkey_btn_show.state(["!disabled"])
        self.pubkey_btn_save.state(["disabled"])

    def seckey_open(self, *args):
        file_path = filedialog.askopenfile(
            defaultextension=".pem",
            filetypes=[("Key types", ".pem")],
            initialdir=KEYS_DIR,
        )
        if file_path is None or file_path.name == "":
            return False

        if not self.cipher.open_seckey(file_path.name):
            messagebox.showerror(
                title=TITLE_ERROR_MESSAGE, message=self.cipher.errormessage
            )
            return False

        self.keylenght.set(self.cipher.keylenght)
        self.seckey.set(self.cipher.key_secret.decode(encoding="utf-8"))
        self.seckey_fname.set(self.cipher.seckey_filename)
        self.seckey_btn_show.state(["!disabled"])
        self.seckey_btn_save.state(["disabled"])

    def pubkey_show(self, *args):
        MessageDialog(title=self.keylenght.get(), prompt=self.pubkey.get())

    def seckey_show(self, *args):
        MessageDialog(title=self.keylenght.get(), prompt=self.seckey.get())
