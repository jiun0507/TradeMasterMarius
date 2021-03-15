import configparser as cfg

import alpaca_trade_api as tradeapi

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
        self.watchlist_id = str(self.get_watchlists()[0].id)

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
        return self.api.list_positions()

    def get_watchlists(self):
        return self.api.get_watchlists()

    def get_watchlist(self, watchlist_id):
        return self.api.get_watchlist(watchlist_id)

    def get_stocks_in_alpaca_watchlist(self):
        watch_list = self.get_watchlists()
        stocks = []
        rows = self.get_watchlist(watch_list[0].id)
        for row in rows.assets:
            stocks.append(row['symbol'])
        return stocks

    def post_to_watchlist(self, symbol):
        return self.api.add_to_watchlist(symbol=symbol, watchlist_id=self.watchlist_id)

class PolygonInterface(AlpacaInterface):
    def __init__(self):
        super().__init__()

    def get_polygon_financial_statement(self, symbol, limit):
        params = {}
        params['limit'] = limit
        financial_statement = self.api.polygon.get(path='/reference/financials/'+symbol, params=params, version='v2')
        return financial_statement['results']

    def get_polygon_ticker_symbols(self, pages, perpage=50):
        params = {
            'market': 'STOCKS',
            'page': pages,
            # 'perpage': perpage,
            'active': 'true',
        }
        data = self.api.polygon.get(path='/reference/tickers', params=params, version='v2')
        tickers = data['tickers']
        return tickers

    def get_polygon_company_info(self, symbol):
        try:
            company_detail = self.api.polygon.get(path=f'/meta/symbols/{symbol}/company', version='v1')
        except:
            return None
        return company_detail

    def get_snapshot_of_tickers(self):

        return self.api.polygon.get(path=f'/snapshot/locale/us/markets/stocks/tickers', version='v2')

    def get_snapshot_of_ticker(self, ticker):

        return self.api.polygon.get(path=f'/snapshot/locale/us/markets/stocks/tickers/{ticker}', version='v2')

    def get_last_quote_of_ticker(self, ticker):

        return self.api.polygon.get(path=f'/last_quote/stocks/{ticker}', version='v1')

    def get_last_trade_of_ticker(self, ticker):

        return self.api.polygon.get(path=f'/last/stocks/{ticker}', version='v1')

    def get_market_status(self):
        status = self.api.polygon.get(path=f'/marketstatus/now', version='v1')
        return status['market']
