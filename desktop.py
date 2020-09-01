from tkinter import *
from tkinter import ttk

from financial_data_use_case import FinancialDataUseCase, TrackingUseCase


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
            command=self._read_company_info_from_ticker_db,
            entry=self.entry,
        )

        self.read_ticker_button = self._add_button(
            text="Read Tickers",
            row=3,
            column=1,
            entry=self.entry,
            command=self._read_all_tickers,
        )

        # self.fs_store_button = self._add_button(
        #     text="fs_store",
        #     row=4,
        #     column=1,
        #     entry=self.entry,
        #     command=self._upload_financial_statements_from_companies,
        # )
        self.test_button = self._add_button(
            text="snapshot",
            row=5,
            column=1,
            entry=self.entry,
            command=self._snapshot,
        )
        self.root.mainloop()

    def _read_company_info_from_ticker_db(self, entry, button=None):

        total = int(entry.get())
        entry.delete(0, END)
        FinancialDataUseCase().store_company_information_from_ticker_table(total=total)

    def _read_all_tickers(self, entry=None, button=None):
        pages = 1
        if entry:
            pages = int(entry.get())
            entry.delete(0, END)

        FinancialDataUseCase().store_all_possible_ticker_symbols(pages=pages)


    def _snapshot(self, button=None):
        TrackingUseCase()._run_tracking_and_store_financial_data(wait_time_minutes=5)

    # def _upload_financial_statements_from_companies(self, button=None):
    #         tickers = AlpacaInterface().read_tickers(limit=10, offset=0)
    #         for ticker in tickers:
    #             result = AlpacaView(AlpacaUseCase(AlpacaInterface())).get_financial_statement(ticker)
    #             AlpacaInterface().store_financial_statement(result[0])
