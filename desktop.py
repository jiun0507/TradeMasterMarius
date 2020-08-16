import json
from tkinter import *

from alpaca_repository import AlpacaRepository
from alpaca_use_case import AlpacaUseCase
from handler import AlpacaView, TelegramInterface


class BaseWindow:
    def __init__(self, width=None, height=None):
        self.root = Tk()

    def _add_label(self, text, row=None, column=None, font=None):
        label = Label(self.root, text=text, font=font)
        label.grid(row=row, column=column)
        label.pack()
        return label

    def _add_button(self, text, fg=None, bg=None, row=None, column=None, command=None, entry=None):
        composed_command = lambda:command(entry) if command and entry else None
        button = Button(self.root, fg=fg, bg=bg, text=text, command=composed_command)
        button.grid(row=row, column=column)
        button.pack()
        return button

    def _add_entry(self, width=None, borderwidth=None, font=None, columnspan=None, padx=None, pady=None, row=None, column=None):
        entry = Entry(self.root, width=width, borderwidth=borderwidth, font=font)
        entry.grid(columnspan=columnspan, padx=padx, pady=pady, row=row, column=column)
        entry.pack()
        return entry


class LandingWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.root.title("Marius.com")
        self.root.geometry("400x400")
        self._add_label(text="Welcome to Marius Stocks", row=0, column=1, font=('Helvetica', 24))
        self.entry = self._add_entry(width=30, borderwidth=10, columnspan=3, row=1)
        self._add_button(
            text="Go to Stocks",
            row=2,
            column=1,
            command=self._command_find_stock,
            entry=self.entry,
        )
        self.root.mainloop()

    def _command_find_stock(self, entry):
        value = entry.get()
        entry.delete(0, END)
        if value == 'Alpaca Balance':
            result = AlpacaView(AlpacaUseCase(AlpacaRepository())).get()
            Label(self.root, text=result).pack()
        else:
            result = AlpacaView(AlpacaUseCase(AlpacaRepository())).get_financial_statement(value)[0]
            Label(self.root, text=json.dumps(result), wraplength=250).pack()
