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
        if not company_details or len(company_details) == 0:
            print('There is no information.')
            return None
        post_body = []
        for company_detail in company_details:
            post_body.append(
                (
                    company_detail.get('symbol', None),
                    company_detail.get('logo', None),
                    company_detail.get('exchange', None),
                    company_detail.get('name', None),
                    company_detail.get('cik', None),
                    company_detail.get('bloomberg', None),
                    company_detail.get('lei', None),
                    company_detail.get('sic', None),
                    company_detail.get('country', None),
                    company_detail.get('industry', None),
                    company_detail.get('sector', None),
                    company_detail.get('marketcap', None),
                    company_detail.get('employees', None),
                    company_detail.get('phone', None),
                    company_detail.get('ceo', None),
                    company_detail.get('url', None),
                    company_detail.get('description', None),
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

    def snapshot_all_tickers(self):

        return self.api.polygon.get(path=f'/snapshot/locale/us/markets/stocks/tickers', version='v2')

    def store_financial_statement(self, fs):
        fs_time = (
            None,
            fs.get('data_source', 'polygon'),
            fs.get('ticker', None),
            fs.get('period', None),
            fs.get('calendarDate', None),
            fs.get('reportPeriod', None),
            fs.get('updated', None),
        )

        fs_indices = (
                None,
                None,
                fs.get('ticker', None),
                fs.get('enterpriseValue', None),
                fs.get('enterpriseValueOverEBIT', None),
                fs.get('enterpriseValueOverEBITDA', None),
                fs.get('payoutRatio', None),
                fs.get('priceToBookValue', None),
                fs.get('priceEarnings', None),
                fs.get('priceToEarnings', None),
                fs.get('priceToEarningsRatio', None),
                fs.get('preferredDividendsIncomeStatementImpact', None),
                fs.get('sharePriceAdjustedClose', None),
                fs.get('priceSales', None),
                fs.get('priceToSalesRatio', None),
                fs.get('returnOnAverageAssets', None),
                fs.get('returnOnAverageEquity', None),
                fs.get('returnOnInvestedCapital', None),
                fs.get('returnOnSales', None),
                fs.get('shares', None),
                fs.get('weightedAverageShares', None),
                fs.get('weightedAverageSharesDiluted', None),
                fs.get('salesPerShare', None),
                fs.get('tangibleAssetsBookValuePerShare', None),
        )
        self.db.post_many(
            {
                'fs_time': str(Query.into('FSTime').insert(fs_time)),
                'fs_indices': str(Query.into('FSIndices').insert(fs_indices)),
            },
        )
