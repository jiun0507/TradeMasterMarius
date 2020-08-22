import configparser as cfg
import json
from socket import create_connection

import alpaca_trade_api as tradeapi
import requests

from sqlite import sqlite
from pypika import Query, Table, Field
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
        return financial_statement['results']

    def get_position_list(self):
        positions = self.api.list_positions()
        return positions

    def get_polygon_supported_ticker_symbols(self, pages):
        for page in range(1, 700):
            params = {
                'market': 'STOCKS',
                'page': page,
            }
            data = self.api.polygon.get(path='/reference/tickers', params=params, version='v2')
            tickers = data['tickers']
            ticker_list = []
            for ticker in tickers:
                ticker_list.append((ticker['ticker'],))
            self.create_tickers(ticker_list)
        return "Stored tickers onto db."

    def read_company_info(self, symbol):
        try:
            company_detail = self.api.polygon.get(path=f'/meta/symbols/{symbol}/company', version='v1')
            print(company_detail['name'])
        except:
            print('error')
            return None
        return company_detail

    def create_company_info(self, company_detail):
        if not company_detail:
            return None
        return self.db.post(str(Query.into('Company').replace(
            company_detail['symbol'],
            company_detail['logo'],
            company_detail['exchange'],
            company_detail['name'],
            company_detail['cik'],
            company_detail['bloomberg'],
            company_detail['lei'],
            company_detail['sic'],
            company_detail['country'],
            company_detail['industry'],
            company_detail['sector'],
            company_detail['marketcap'],
            company_detail['employees'],
            company_detail['phone'],
            company_detail['ceo'],
            company_detail['url'],
            company_detail['description'],
        )))

    def create_company_informations(self, company_details):
        if len(company_details) > 100:
            print('This is too much information to load.')
            return None
        if not company_details:
            print('There is no information.')
            return None
        post_body = []
        for company_detail in company_details:
            post_body.append(
                (
                    getattr(company_detail, 'symbol', None),
                    getattr(company_detail, 'logo', None),
                    getattr(company_detail, 'exchange', None),
                    getattr(company_detail, 'name', None),
                    getattr(company_detail, 'cik', None),
                    getattr(company_detail, 'bloomberg', None),
                    getattr(company_detail, 'lei', None),
                    getattr(company_detail, 'sic', None),
                    getattr(company_detail, 'country', None),
                    getattr(company_detail, 'industry', None),
                    getattr(company_detail, 'sector', None),
                    getattr(company_detail, 'marketcap', None),
                    getattr(company_detail, 'employees', None),
                    getattr(company_detail, 'phone', None),
                    getattr(company_detail, 'ceo', None),
                    getattr(company_detail, 'url', None),
                    getattr(company_detail, 'description', None),
                ),
            )
        return self.db.post_many(
            [
                str(Query.into('Company').insert(body)) for body in post_body
            ],
        )

    def create_tickers(self, tickers: list):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        sql = ''' INSERT OR REPLACE INTO Tickers(Symbol)
                VALUES(?) '''
        self.db.post_many(sql, tickers)

    def read_tickers(self, limit=None, offset=None):
        query = Query.from_('Tickers').select('*')
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return self.db.get(str(query))


