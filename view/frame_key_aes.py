from tkinter import ttk, filedialog, messagebox, StringVar
from model.aes_cipher import AESCipher
from constant import (
    LABEL_KEY_AES_NEEDSAVE,
    LABEL_KEY_AES_INIT,
    AES_KEYLENGHT_DICT,
    BTN_GENERATE_KEY,
    BTN_OPEN_KEY,
    BTN_SAVE_KEY,
    KEYS_DIR,
    TITLE_ERROR_MESSAGE,
)


class FrameKeyAES:
    def __init__(self, master):
        self.cipher = AESCipher()

        self.key = StringVar()
        self.filename = StringVar(value=LABEL_KEY_AES_INIT)
        self.keylenght = StringVar()
        self.btn_save = None

        self.frame_draw(master)

    """ AES Frame """

    def frame_draw(self, master):
        master.columnconfigure(2, weight=3)

        combo = ttk.Combobox(
            master,
            width=10,
            values=list(AES_KEYLENGHT_DICT.keys()),
            textvariable=self.keylenght,
            state="readonly",
        )
        combo.current(0)
        combo.grid(row=0, column=0, sticky="we", pady=[0, 5])

        entry = ttk.Entry(master, width=75, textvariable=self.key, state="readonly")
        entry.grid(row=0, column=1, columnspan=3, sticky="we", padx=[5, 0], pady=[0, 5])

        ttk.Button(
            master, width=11, text=BTN_GENERATE_KEY, command=self.key_generate
        ).grid(row=1, column=0, sticky="w")
        ttk.Button(master, text=BTN_OPEN_KEY, command=self.key_open).grid(
            row=1, column=1, sticky="w", padx=[5, 0]
        )

        entry_filename = ttk.Entry(
            master, width=30, textvariable=self.filename, state="readonly"
        )
        entry_filename.grid(row=1, column=2, sticky="we", padx=[5, 0])

        self.btn_save = ttk.Button(
            master, text=BTN_SAVE_KEY, command=self.key_save, state=["disabled"]
        )
        self.btn_save.grid(row=1, column=3, sticky="e", padx=[5, 0])

    """ Comands """

    def key_generate(self, *args):
        block_size = AES_KEYLENGHT_DICT[self.keylenght.get()]
        key = self.cipher.generate_key(block_size=block_size)
        self.key.set(key)
        self.filename.set(LABEL_KEY_AES_NEEDSAVE)
        self.btn_save.state(["!disabled"])

    def key_save(self, *args):
        if self.key.get() == "":
            return False

        print(self.keylenght.get())
        filename = self.cipher.key_filename_generate(keylenght=self.keylenght.get())
        file_path = filedialog.asksaveasfile(
            defaultextension=".pem",
            filetypes=[("Key types", ".pem")],
            initialdir=KEYS_DIR,
            initialfile=filename,
        )
        if file_path is None or file_path.name == "":
            return False

        self.cipher.save_key(file_path=file_path.name)
        self.filename.set(self.cipher.filename)
        self.btn_save.state(["disabled"])

    def key_open(self, *args):
        file_path = filedialog.askopenfile(
            defaultextension=".pem",
            filetypes=[("Key types", ".pem")],
            initialdir=KEYS_DIR,
        )
        if file_path is None or file_path.name == "":
            return False

        key, keylenght = self.cipher.open_key(file_path.name)
        if not key or not keylenght:
            messagebox.showerror(
                title=TITLE_ERROR_MESSAGE, message=self.cipher.errormessage
            )
            return False

        self.key.set(key)
        self.keylenght.set(keylenght)
        self.filename.set(self.cipher.filename)
        self.btn_save.state(["disabled"])
