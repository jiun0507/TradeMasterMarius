from tkinter import *


class Window:
    def __init__(self, width=None, height=None):
        self.root = Tk()
        self.root.title("Marius.com")
        self.root.geometry("400x400")
        self._add_label(text="This is the first try!", row=0, column=1, font=('Helvetica', 24))
        self._add_button(
            text="try clicking!",
            row=2,
            column=1,
            command=self.print_x,
            entry=self._add_entry(width=30, borderwidth=10, columnspan=3, row=1),
        )
        self.root.mainloop()

    def print_x(self, x):
        Label(self.root, text=x).pack()

    def _add_label(self, text, row=None, column=None, font=None):
        label = Label(self.root, text=text, font=font)
        label.grid(row=row, column=column)
        label.pack()
        return label

    def _add_button(self, text, fg=None, bg=None, row=None, column=None, command=None, entry=None):
        composed_command = lambda:command(entry.get()) if command and entry else None
        button = Button(self.root, fg=fg, bg=bg, text=text, command=composed_command)
        button.grid(row=row, column=column)
        button.pack()
        return button

    def _add_entry(self, width=None, borderwidth=None, font=None, columnspan=None, padx=None, pady=None, row=None, column=None):
        entry = Entry(self.root, width=width, borderwidth=borderwidth, font=font)
        entry.grid(columnspan=columnspan, padx=padx, pady=pady, row=row, column=column)
        entry.pack()
        return entry



window = Window()
