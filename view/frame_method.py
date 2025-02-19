from tkinter import ttk, StringVar
from inner_state import InnerState
from constant import METHODS_LIST


class FrameMethod:
    def __init__(self, master):
        self.state = InnerState()
        self.method = StringVar()
        self.method.set(self.state.cipher_method)

        self.frame_draw(master)

    def frame_draw(self, master):
        method_combo = ttk.Combobox(
            master, values=METHODS_LIST, textvariable=self.method, state="readonly"
        )
        method_combo.grid(row=0, column=1, sticky="we")
        method_combo.bind("<<ComboboxSelected>>", self.method_select)

    """ Comands """

    def method_select(self, *args):
        self.state.cipher_method = self.method.get()
