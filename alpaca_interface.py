import configparser as cfg
import json
from socket import create_connection

import alpaca_trade_api as tradeapi
import requests

from sqlite import sqlite
from pypika import Query, Table, Field
config = ".config.cfg"


class AlpacaInterface:
    def __init__(self):
        self.alpaca_api_id = self.read_key_from_config_file(config, 'alpaca_api_id')
        self.alpaca_key = self.read_key_from_config_file(config, 'alpaca_key')

        self.api = tradeapi.REST(
            self.alpaca_api_id,
            self.alpaca_key,
            'https://paper-api.alpaca.markets',
            api_version='v2',
        )

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

    def get_position_list(self):
        positions = self.api.list_positions()
        return positions

class PolygonInterface(AlpacaInterface):
    def __init__(self):
        super().__init__()

    def get_polygon_financial_statement(self, symbol, limit):
        params = {}
        params['limit'] = limit
        financial_statement = self.api.polygon.get(path='/reference/financials/'+symbol, params=params, version='v2')
        return financial_statement['results']

    def get_polygon_ticker_symbols(self, pages):
        ticker_list = []
        for page in range(1, pages):
            params = {
                'market': 'STOCKS',
                'page': page,
            }
            data = self.api.polygon.get(path='/reference/tickers', params=params, version='v2')
            tickers = data['tickers']
            for ticker in tickers:
                ticker_list.append((ticker['ticker'],))
        return ticker_list

    def get_polygon_company_info(self, symbol):
        try:
            company_detail = self.api.polygon.get(path=f'/meta/symbols/{symbol}/company', version='v1')
        except:
            return None
        return company_detail

    def get_snapshot_of_tickers(self):

        return self.api.polygon.get(path=f'/snapshot/locale/us/markets/stocks/tickers', version='v2')