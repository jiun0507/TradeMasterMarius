import configparser as cfg
import json
from socket import create_connection

import alpaca_trade_api as tradeapi
import requests

from sqlite import sqlite

config = ".config.cfg"
class AlpacaRepository:
    def __init__(self):
        self.alpaca_api_id = self.read_key_from_config_file(config, 'alpaca_api_id')
        self.alpaca_key = self.read_key_from_config_file(config, 'alpaca_key')

        self.api = tradeapi.REST(
            self.alpaca_api_id,
            self.alpaca_key,
            'https://paper-api.alpaca.markets',
            api_version='v2',
        )
        self.db = sqlite('marius.db')

    def read_key_from_config_file(self, config, key):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', key)

    def get_account_info(self):
        # Get our account information.
        account = self.api.get_account()

        # Check our current balance vs. our balance at the last market close
        balance_change = float(account.equity) - float(account.last_equity)
        return 'Today\'s portfolio balance change:{}'.format(balance_change)

    def get_polygon_financial_statement(self, symbol, limit):
        params = {}
        params['limit'] = limit
        financial_statement = self.api.polygon.get(path='/reference/financials/'+symbol, params=params, version='v2')
        return financial_statement

    def get_position_list(self):
        positions = self.api.list_positions()
        return positions

    def get_polygon_supported_ticker_symbols(self):
        params = {
            'market': 'STOCKS',
            'page': 1,
        }
        tickers = self.api.polygon.get(path='/reference/tickers', params=params, version='v2')['tickers']
        ticker_list = []
        for ticker in tickers:
            ticker_list.append((ticker['ticker'],))
        self.create_tickers(ticker_list)
        return ticker_list

    def create_tickers(self, tickers: list):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        print(tickers)
        sql = ''' INSERT INTO Tickers(Symbol)
                VALUES(?) '''
        self.db.post_many(sql, tickers)