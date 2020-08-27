from alpaca_interface import AlpacaInterface, PolygonInterface
from financial_statement_repository import FinancialStatementRepository
from ticker_repository import TickerRepository
from company_repository import CompanyRepository

polygon = PolygonInterface()

class FinancialDataUseCase:
    def __init__(self) -> None:
        self._ticker_repo = TickerRepository()
        self._financial_statement_repo = FinancialStatementRepository()
        self._company_repo = CompanyRepository()

    def store_all_possible_ticker_symbols(self, pages=None):
        for page in range(0, pages):
            ticker_set = polygon.get_polygon_ticker_symbols(pages=page, perpage=50)
            print(page, len(ticker_set), ticker_set)
            self._ticker_repo.post_many(ticker_set)

    def store_financial_statement(self, symbol=None):
        if not symbol:
            return None
        financial_statement = polygon.get_polygon_financial_statement(symbol=symbol)
        return self._financial_statement_repo.post(financial_statement)

    def _get_many_tickers(self, offset=None, limit=None):
        return self._ticker_repo.get_many(offset, limit)

    def store_company_information_from_ticker_table(self, offset=0, limit=20, total = 34277):
        offset = 9980
        while offset < total:
            print('the start:', offset)
            tickers = self._ticker_repo.get_many(offset=offset, limit=limit)
            company_details = []
            for ticker in tickers:
                company_detail = polygon.get_polygon_company_info(symbol=ticker.symbol)
                if company_detail:
                    company_details.append(company_detail)
            self._company_repo.post_many(company_details)
            offset += limit
        return


class TrackingUseCase:
    def __init__(self):
        self._alpaca_interface = AlpacaInterface()
        self._polygon_interface = PolygonInterface()
        watchlists = self._alpaca_interface.get_watchlists()
        self.stocks_on_watchlists = []
        for watchlist in watchlists:
            watchlist_entity = self._alpaca_interface.get_watchlist(watchlist.id)
            self.stocks_on_watchlists += watchlist_entity.assets

    def _get_snapshot(self):
        snapshot = self._polygon_interface.get_snapshot_of_tickers()

        tickers = snapshot['tickers']

        for stock in self.stocks_on_watchlists:
            match = next((ticker for ticker in tickers if ticker['ticker'] == stock['symbol']), None)
