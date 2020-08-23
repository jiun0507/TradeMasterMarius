import json
from tkinter import *
from tkinter import ttk

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
        if command and entry:
            composed_command = lambda:command(entry)
        else:
            composed_command = command
        # Use ttk.Button instead of tkinter.Button because of text visibility issue
        button = ttk.Button(self.root, fg=fg, bg=bg, text=text, command=composed_command)
        button.grid(row=row, column=column)
        button.pack()
        return button

    def _add_entry(self, width=None, borderwidth=None, font=None, columnspan=None, padx=None, pady=None, row=None, column=None):
        entry = Entry(self.root, width=width, borderwidth=borderwidth, font=font)
        entry.grid(columnspan=columnspan, padx=padx, pady=pady, row=row, column=column)
        entry.pack()
        return entry

    @staticmethod
    def _disable(button=None, label=None):
        if button:
            button.config(state='disable')
        if label:
            label.config(state='disable')

    @staticmethod
    def _enable(button=None, label=None):
        if button:
            button.config(state='normal')
        if label:
            label.config(state='normal')


class LandingWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.root.title("Marius.com")
        self.root.geometry("400x400")
        self._add_label(text="Welcome to Marius Stocks", row=0, column=1, font=('Helvetica', 24))
        self.entry = self._add_entry(width=30, borderwidth=10, columnspan=3, row=1)
        self.find_stock_button = self._add_button(
            text="Go to Stocks",
            row=2,
            column=1,
            command=self._command_find_stock,
            entry=self.entry,
        )
        self.read_ticker_button = self._add_button(
            text="Read Tickers",
            row=3,
            column=1,
            entry=self.entry,
            command=self._read_all_tickers,
        )
        self.test_button = self._add_button(
            text="snapshot",
            row=4,
            column=1,
            entry=self.entry,
            command=self._snapshot,
        )
        self.root.mainloop()

    def _command_find_stock(self, entry, button=None):
        if self.find_stock_button['text'] == 'Go to Stocks':
            value = entry.get()
            entry.delete(0, END)
            if value == 'Alpaca Balance':
                result = AlpacaView(AlpacaUseCase(AlpacaRepository())).get()
                Label(self.root, text=result).pack()
            else:
                result = AlpacaView(AlpacaUseCase(AlpacaRepository())).get_financial_statement(value)[0]
                Label(self.root, text=json.dumps(result), wraplength=250).pack()
            self.find_stock_button['text'] = 'Here it is'
        else:
            self._enable(button=self.find_stock_button)
            entry.delete(0, END)
            self.find_stock_button['text'] = 'Go to Stocks'

    def _read_all_tickers(self, entry=None, button=None):
        start = 3050
        limit = 50
        total = 10
        if entry:
            total = int(entry.get())
            entry.delete(0, END)
        for step in range(total//limit + 1):
            offset = step*limit + start
            tickers = AlpacaRepository().read_tickers(limit=limit, offset=offset)
            company_details = []
            for ticker in tickers:
                print(ticker)
                company_detail = AlpacaRepository().read_company_info(ticker)
                if company_detail:
                    company_details.append(company_detail)

            AlpacaRepository().create_company_informations(company_details)

    def _snapshot(self, button=None):
        snapshot = AlpacaRepository().snapshot_all_tickers()
        print(snapshot)

    def _upload_financial_statements_from_companies(self, entry=None, button=None):
        start = 0
        limit = 50
        total = 10
        if entry:
            total = int(entry.get())
            entry.delete(0, END)
        for step in range(total//limit + 1):
            offset = step*limit + start
            tickers = AlpacaRepository().read_tickers(limit=limit, offset=offset)
            financial_statements = []
            for ticker in tickers:
                print(ticker)
                result = AlpacaView(AlpacaUseCase(AlpacaRepository())).get_financial_statement(ticker)[0]
                if result:
                    financial_statements.append(result)

            AlpacaRepository().store_financial_statement(financial_statements)