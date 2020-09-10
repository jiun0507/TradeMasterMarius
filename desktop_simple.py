#!/usr/bin/env python
import PySimpleGUI as sg
import random
import string
from models import FinancialStatement
from financial_data_use_case import FinancialDataUseCase
"""
    Basic use of the Table Element
"""

sg.theme('Dark Green')


class FSTableViewJob:
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
                    print(row)
                    self.data.append(row)
                self.window['-TABLE-'].update(values=self.data)
            elif event == 'Change Colors':
                self.window['-TABLE-'].update(row_colors=((8, 'white', 'blue'), (9, 'green')))

        self.window.close()

FSTableViewJob().run()