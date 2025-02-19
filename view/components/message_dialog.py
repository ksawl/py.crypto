from tkinter import Text, LEFT, Scrollbar, Y, WORD, Frame, Button, ACTIVE
from tkinter.simpledialog import Dialog


class MessageDialog(Dialog):
    def __init__(self, title, prompt, parent=None):
        self.prompt = prompt

        Dialog.__init__(self, parent, title)

    def destroy(self):
        self.entry = None
        Dialog.destroy(self)

    def body(self, master):
        text = Text(master, width=65, height=20, wrap=WORD, padx=20)
        text.pack(side=LEFT)
        text.insert(1.0, self.prompt)
        text["state"] = "disabled"

        scroll = Scrollbar(master, command=text.yview)
        scroll.pack(side=LEFT, fill=Y)
        text.config(yscrollcommand=scroll.set)

    def buttonbox(self):
        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.cancel, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.ok)

        box.pack()

    def validate(self):
        return 1
