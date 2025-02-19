from tkinter import ttk, filedialog, messagebox, StringVar, Text, END
from model.aes_cipher import AESCipher
from model.rsa_cipher import RSACipher
from model.sign_cipher import SignCipher
from utils.file_crud import FileCRUD
from inner_state import InnerState
from constant import (
    TITLE_ERROR_MESSAGE,
    LABEL_FROM_TEXT_RADIO,
    LABEL_FROM_FILE_RADIO,
    BTN_OPEN_KEY,
    LABEL_SIGN_CHECK,
    BTN_DECRYPT,
    TITLE_INFO_MESSAGE,
    INFO_COPY_CLIPBOARD_OK,
    ENCRYPT_DIR,
    ERROR_UNKNOWN,
    ERROR_IS_NO_TEXT,
    ERROR_IS_NO_FILE,
    ERROR_DECODE,
)


class FrameDecrypt:
    def __init__(self, master):
        self.state = InnerState()

        self.aes_cipher = AESCipher()
        self.rsa_cipher = RSACipher()
        self.sign_cipher = SignCipher()

        self.from_decode_vals = ["text", "file"]
        self.from_decode = StringVar(value=self.from_decode_vals[0])
        self.filepath_input = ""
        self.file_input = StringVar()
        self.file_output = StringVar()
        self.sign_check = StringVar()
        self.btn_file_input = None

        self.frame_draw(master)

    def frame_draw(self, master):
        text_radio = ttk.Radiobutton(
            master,
            variable=self.from_decode,
            value=self.from_decode_vals[0],
            text=LABEL_FROM_TEXT_RADIO,
            command=self.from_decode_select,
        )
        text_radio.grid(row=0, column=0, sticky="nsew")

        text_frame = ttk.Frame(master)
        text_frame.grid(row=1, column=0, sticky="nsew", pady=[0, 5])

        self.ciphertext_text = Text(text_frame, width=43, height=5)
        self.ciphertext_text.grid(row=0, column=0, sticky="w")
        self.ciphertext_text.bind("<Button-3>", self.clean_text)

        self.decrypted_text = Text(text_frame, width=43, height=5, state="disabled")
        self.decrypted_text.grid(row=0, column=1, sticky="e")
        self.decrypted_text.bind("<ButtonPress>", self.copy_to_clipboard)
        self.decrypted_text.bind("<Button-3>", self.clean_text)

        file_radio = ttk.Radiobutton(
            master,
            variable=self.from_decode,
            value=self.from_decode_vals[1],
            text=LABEL_FROM_FILE_RADIO,
            command=self.from_decode_select,
        )
        file_radio.grid(row=2, column=0, sticky="nsew")

        file_frame = ttk.Frame(master)
        file_frame.grid(row=3, column=0, sticky="nsew", pady=[0, 5])

        self.btn_file_input = ttk.Button(
            file_frame,
            text=BTN_OPEN_KEY,
            command=self.open_file_input,
            state="disabled",
        )
        self.btn_file_input.grid(row=0, column=0, sticky="w")

        file_input_entry = ttk.Entry(
            file_frame, width=37, textvariable=self.file_input, state="readonly"
        )
        file_input_entry.grid(row=0, column=1, sticky="we", padx=[5, 0])

        file_output_entry = ttk.Entry(
            file_frame, width=37, textvariable=self.file_output, state="readonly"
        )
        file_output_entry.grid(row=0, column=2, sticky="we", padx=[5, 0])

        sign_frame = ttk.Frame(master)
        sign_frame.grid(row=4, column=0, sticky="e")

        sign_checkbox = ttk.Checkbutton(
            sign_frame, text=LABEL_SIGN_CHECK, variable=self.sign_check
        )
        sign_checkbox.grid(row=0, column=0, sticky="e", padx=[0, 10])

        ttk.Button(sign_frame, text=BTN_DECRYPT, command=self.decrypt).grid(
            row=0, column=1, sticky="e"
        )

    """ Binds """

    def copy_to_clipboard(self, event):
        text = event.widget.get("1.0", END)
        if len(text) > 1:
            event.widget.clipboard_clear()
            event.widget.clipboard_append(text)
            messagebox.showinfo(
                title=TITLE_INFO_MESSAGE, message=INFO_COPY_CLIPBOARD_OK
            )

    def clean_text(self, event):
        widget_state = event.widget["state"]
        if widget_state == "disabled":
            event.widget["state"] = "normal"

        event.widget.delete("1.0", END)

        if widget_state == "disabled":
            event.widget["state"] = "disabled"

    """ Commands """

    def from_decode_select(self, *args):
        if self.from_decode.get() == self.from_decode_vals[0]:
            self.btn_file_input.state(["disabled"])
            self.file_input.set("")
            self.file_output.set("")
            self.filepath_input = ""
            self.ciphertext_text["state"] = "normal"
        else:
            self.btn_file_input.state(["!disabled"])
            self.ciphertext_text.delete("1.0", END)
            self.ciphertext_text["state"] = "disabled"
            self.decrypted_text["state"] = "normal"
            self.decrypted_text.delete("1.0", END)
            self.decrypted_text["state"] = "disabled"

    def open_file_input(self, *args):
        file_path = filedialog.askopenfile(
            defaultextension=".*",
            filetypes=[("All types", ".*")],
            initialdir=ENCRYPT_DIR,
        )
        if file_path is not None and file_path.name != "":
            self.file_input.set(FileCRUD.path_basename(file_path.name))
            self.filepath_input = file_path.name

    def decrypt(self, *args):
        errormessage = ERROR_UNKNOWN
        self.decrypted_text["state"] = "normal"
        self.decrypted_text.delete("1.0", END)
        self.file_output.set("")

        """ Get data """
        if self.from_decode.get() == self.from_decode_vals[0]:
            text = self.ciphertext_text.get("1.0", END)
            if len(text) == 1:
                return messagebox.showerror(
                    title=TITLE_ERROR_MESSAGE, message=ERROR_IS_NO_TEXT
                )

            ciphertext = text.encode()
        else:
            if self.filepath_input == "":
                return messagebox.showerror(
                    title=TITLE_ERROR_MESSAGE, message=ERROR_IS_NO_FILE
                )

            ciphertext = FileCRUD.read_file(self.filepath_input)

        """ Signature """
        decrypt_result = False
        if self.sign_check.get() == "1":
            decrypt_result = self.sign_cipher.verify_sign(ciphertext)
            errormessage = self.sign_cipher.errormessage
            if decrypt_result is not False:
                ciphertext = decrypt_result

        """ Decrypt """
        if ciphertext is not False:
            if self.state.cipher_method == "AES":
                decrypt_result = self.aes_cipher.decrypt_CBC(ciphertext)
                errormessage = self.aes_cipher.errormessage
            elif self.state.cipher_method == "RSA":
                decrypt_result = self.rsa_cipher.decrypt(ciphertext)
                errormessage = self.rsa_cipher.errormessage
            elif self.state.cipher_method == "AES+RSA":
                aes_key_encrypt, data_encrypt = self.rsa_cipher.split_encrypted_data(
                    ciphertext
                )
                rsa_decrypt_result = self.rsa_cipher.decrypt(aes_key_encrypt)
                errormessage = self.rsa_cipher.errormessage

                if data_encrypt is not False and rsa_decrypt_result is not False:
                    self.aes_cipher.key = rsa_decrypt_result
                    aes_decrypt_result = self.aes_cipher.decrypt_CBC(data_encrypt)
                    errormessage = self.aes_cipher.errormessage

                    if aes_decrypt_result is not False:
                        decrypt_result = aes_decrypt_result

        """ Return Error """
        if decrypt_result is False:
            return messagebox.showerror(title=TITLE_ERROR_MESSAGE, message=errormessage)

        """ Return data """
        try:
            if self.from_decode.get() == self.from_decode_vals[0]:
                self.decrypted_text.insert("1.0", decrypt_result.decode())
                self.decrypted_text["state"] = "disabled"
            else:
                new_file_path = FileCRUD.path_decrypt_file(self.filepath_input)
                new_filename = FileCRUD.write_file(new_file_path, decrypt_result)
                self.file_output.set(new_filename)

        except UnicodeDecodeError:
            return messagebox.showerror(title=TITLE_ERROR_MESSAGE, message=ERROR_DECODE)
