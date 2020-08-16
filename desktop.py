from tkinter import *


class Window:
    def __init__(self):
        self.root = Tk()
        self._add_label(text="This is the first try!", row=0, col=0)
        self._add_button(text="try clicking!")
        self._add_entry(width=10, height=10)
        self.root.mainloop()

    def _add_label(self, text, row=None, col=None):
        label = Label(self.root, text=text)
        label.pack()
        return label

    def _add_button(self, text, row=None, col=None, command=None, entry=None):
        button = Button(self.root, text=text, command=command)
        button.pack()
        return button

    def _add_entry(self, width=None, height=None):
        entry = Entry(self.root)
        entry.pack()
        return entry

window = Window()
