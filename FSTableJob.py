#!/usr/bin/env python
from signal_handler import ProgramKilled
from watchlist_repository import WatchlistRepository
import PySimpleGUI as sg
from models import FinancialStatement, WatchList
from financial_data_use_case import FinancialDataUseCase
from alpaca_interface import AlpacaInterface, PolygonInterface
import time
import abc
"""
    Basic use of the Table Element
"""

sg.theme('Dark Green')

class WatchListView:
    # ------ Some functions to help generate data for the table ------

    def find_table_columns(self):
        return WatchList.__table__.columns.keys()

    def get_rows_from_watchlist(self):
        return self.watchlist_repository.get_all()

    def make_table(self):
        rows = self.get_rows_from_watchlist()
        data = [[j for j in range(3)] for i in range(len(rows)+1)]
        data[0] = ['symbol', 'expected_price']

        for i in range(1, len(rows)+1):
            data[i] = rows[i-1]
        return data

    def get_alpaca_watchlist(self):
        watch_list = self.alpaca_interface.get_watchlists()
        stocks = []
        rows = self.alpaca_interface.get_watchlist(watch_list[0].id)
        for row in rows.assets:
            stocks.append(row.symbol)
        return stocks

    def __init__(self):
        # ------ Initialize the table ------
        self.alpaca_interface = AlpacaInterface()
        self.polygon_interface = PolygonInterface()
        self.watchlist_repository= WatchlistRepository()
        self.data = self.make_table()
        headings = [str(self.data[0][x]) for x in range(len(self.data[0]))]

        # ------ Window Layout ------
        layout = [[sg.Table(values=self.data[1:][:], headings=headings, max_col_width=25,
                            # background_color='light blue',
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='right',
                            num_rows=20,
                            alternating_row_color='lightyellow',
                            key='-TABLE-',
                            row_height=35,
                            tooltip='This is a table')],
                [sg.Button('Upload'), sg.Button('Delete'), sg.Button('Change Colors')],
                [sg.Text('Upload= Upload one to the Watchlist')],
                [sg.Text('Delete = Delete a stock from the watchlist')],
                [sg.Text('Change Colors = Changes the colors of rows 8 and 9')]]

        # ------ Create Window ------
        self.window = sg.Window('The Table Element', layout,
                        # font='Helvetica 25',
                        )
        self.table_offset = 0

    def run(self):
        # ------ Event Loop ------
        while True:
            event, values = self.window.read()
            print(event, values)
            if event == sg.WIN_CLOSED:
                break
            if event == 'Add':

                self.data = self.make_table()
                self.window['-TABLE-'].update(values=self.data)
            elif event == 'Change Colors':
                self.window['-TABLE-'].update(row_colors=((8, 'white', 'blue'), (9, 'green')))

        self.window.close()


class DealsView:
    # ------ Some functions to help generate data for the table ------

    def find_table_columns(self):
        return WatchList.__table__.columns.keys()

    def get_rows_from_watchlist(self):
        return self.watchlist_repository.get_all()

    def make_table(self):
        rows = self.get_rows_from_watchlist()
        data = [[j for j in range(3)] for i in range(len(rows)+1)]
        data[0] = ['symbol', 'expected_price', 'price']
        for i in range(len(rows)):
            row = rows[i]
            snapshot = self.polygon_interface.get_snapshot_of_ticker(row[0])
            data[i+1] = [
                str(row[0]),
                str(row[1]),
                str(snapshot['ticker']['day']['v']),
            ]
        return data

    def __init__(self):
        # ------ Initialize the table ------
        self.alpaca_interface = AlpacaInterface()
        self.polygon_interface = PolygonInterface()
        self.watchlist_repository= WatchlistRepository()
        self.data = self.make_table()

        headings = [str(self.data[0][x]) for x in range(len(self.data[0]))]

        # ------ Window Layout ------
        layout = [[sg.Table(values=self.data[1:][:], headings=headings, max_col_width=25,
                            # background_color='light blue',
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='right',
                            num_rows=20,
                            alternating_row_color='lightyellow',
                            key='-TABLE-',
                            row_height=35,
                            tooltip='This is a table')],
                [sg.Button('Upload'), sg.Button('Delete'), sg.Button('Change Colors')],
                [sg.Text('Upload= Upload one to the Watchlist')],
                [sg.Text('Delete = Delete a stock from the watchlist')],
                [sg.Text('Change Colors = Changes the colors of rows 8 and 9')]]

        # ------ Create Window ------
        self.window = sg.Window('The Table Element', layout,
                        # font='Helvetica 25',
                        )
        self.table_offset = 0

    def run(self):
        # ------ Event Loop ------
        print("started")
        while True:
            try:
                event, values = self.window.read(timeout=10)
                print(event, values)
                self.data = self.make_table()
                print(self.data)
                self.window['-TABLE-'].update(values=self.data)

            except ProgramKilled:
                print("Program killed: running cleanup code")
                break

        self.window.close()


class FSTableView:
    # ------ Some functions to help generate data for the table ------
    def find_table_columns(self):
        return FinancialStatement.__table__.columns.keys()

    def get_rows_from_fs(self, offset=0, rows=0):
        return FinancialDataUseCase().get_financial_statements(offset, rows)

    # make table
    def make_table(self, offset, num_rows, num_cols):
        data = [[j for j in range(num_cols)] for i in range(num_rows)]
        data[0] = self.find_table_columns()[1:]

        rows = self.get_rows_from_fs(offset, num_rows)
        for i in range(1, len(rows)):
            data[i] = rows[i-1]
        return data
    def __init__(self):
        # ------ Initialize the table ------
        self.data = self.make_table(offset=0, num_rows=15, num_cols=6)
        headings = [str(self.data[0][x]) for x in range(len(self.data[0]))]

        # ------ Window Layout ------
        layout = [[sg.Table(values=self.data[1:][:], headings=headings, max_col_width=25,
                            # background_color='light blue',
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='right',
                            num_rows=20,
                            alternating_row_color='lightyellow',
                            key='-TABLE-',
                            row_height=35,
                            tooltip='This is a table')],
                [sg.Button('Read'), sg.Button('Double'), sg.Button('Change Colors')],
                [sg.Text('Read = read which rows are selected')],
                [sg.Text('Double = double the amount of data in the table')],
                [sg.Text('Change Colors = Changes the colors of rows 8 and 9')]]

        # ------ Create Window ------
        self.window = sg.Window('The Table Element', layout,
                        # font='Helvetica 25',
                        )
        self.table_offset = 0

    def run(self):
        # ------ Event Loop ------
        while True:
            event, values = self.window.read()
            print(event, values)
            if event == sg.WIN_CLOSED:
                break
            if event == 'Double':
                self.table_offset += 15
                new_table = self.make_table(offset=self.table_offset, num_rows=15, num_cols=6)
                for row in new_table[1:]:
                    self.data.append(row)
                print(self.data)
                self.window['-TABLE-'].update(values=self.data)
            elif event == 'Change Colors':
                self.window['-TABLE-'].update(row_colors=((8, 'white', 'blue'), (9, 'green')))

        self.window.close()