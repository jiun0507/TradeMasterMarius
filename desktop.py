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
        composed_command = lambda:command(entry) if command and entry else None
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

    # def btn3func(self):
    #     self.entry.state(['disabled'])
# import tkinter as tk
# from tkinter import ttk

# class entryApp:

#     def __init__(self, master):
#         self.label = ttk.Label(master, text='Enter the text below')
#         self.label.pack()
        
#         self.entry = ttk.Entry(master, width = 30)  # number of characters along the width
#         self.entry.pack()
        
#         self.button = ttk.Button(master, text = "Get Entry")
#         self.button.pack()
#         self.tkstrvar = tk.StringVar()  # create tk string variable
#         self.tkstrvar.set('Nothing is done yet!')   # set the value of tk string variable
#         self.button.config(command = self.getEntry)
        
#         self.msg = ttk.Label(master, text = self.tkstrvar.get())    # get the value of string variable
#         self.msg.pack()
        
#         self.btn1 = ttk.Button(master, text='Delete the entry', command = self.btn1func)
#         self.btn1.pack()
        
#         self.crypt = tk.StringVar()
#         self.crypt.set('Encrypt')
#         self.btn2 = ttk.Button(master, text = "{} Text in Entry Field".format(self.crypt.get()), command = self.changecrypt)
#         self.btn2.pack()
#         #self.entryText = ttk.Entry(master, width=30)
        
#         ttk.Button(master, text = 'Disable Entry Field', command = self.btn3func).pack()
#         ttk.Button(master, text = 'Enable Entry Field', command = self.btn4func).pack()
#         ttk.Button(master, text = 'Readonly Entry Field', command = self.btn5func).pack()
#         ttk.Button(master, text = 'Edit Entry Field', command = self.btn6func).pack()
    
#     def changecrypt(self):
#         if self.crypt.get()=='Encrypt':
#             self.entry.config(show='*')
#             self.crypt.set('Decrypt')
#             self.btn2.config(text = "{} Text in Entry Field".format(self.crypt.get()))
#         else:
#             self.entry.config(show='')
#             self.crypt.set('Encrypt')
#             self.btn2.config(text = "{} Text in Entry Field".format(self.crypt.get()))
    
#     def btn3func(self):
#         self.entry.state(['disabled'])
    
#     def btn4func(self):
#         self.entry.state(['!disabled'])
        
#     def btn5func(self):
#         self.entry.state(['readonly'])
        
#     def getEntry(self):
#         self.tkstrvar.set(self.entry.get())     # get entry widget content and store it in tk_string variable
#         self.msg.config(text = self.tkstrvar.get())   # set msg as value of string variable
        
#     def btn1func(self):
#         self.entry.delete(0, tk.END)    # delete all from 0 to END character in Entry Widget

#     def btn6func(self):
#         self.entry.state(['!readonly'])


# def launchEntryApp():
#     root = tk.Tk()
#     entryApp(root)
#     tk.mainloop()


# def test():
#     launchEntryApp()
            
# if __name__ == '__main__': test()