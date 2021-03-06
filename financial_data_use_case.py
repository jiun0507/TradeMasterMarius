import threading
import time
from datetime import timedelta

# from Interface.alpaca_interface import AlpacaInterface, PolygonInterface
from company_repository import CompanyRepository
from financial_statement_repository import FinancialStatementRepository
from job import Job
from signal_handler import ProgramKilled

# from ticker_repository import TickerRepository
from accountant import Accountant
from Gateway.polygon_gateway import PolygonGateway
from investor import Investor


class FinancialDataUseCase:
    def __init__(self):
        self.accountant = Accountant()
        self.polygon = PolygonGateway(self.accountant)
        self.investor = Investor()
        # self._ticker_repo = TickerRepository()
        # self._financial_statement_repo = FinancialStatementRepository()
        # self._company_repo = CompanyRepository()

    def user_asks_for_evaluation_of_stock(self, security):
        financial_statements = self.polygon.get_polygon_financial_statement(
            security.name, security.limit
        )
        evaluation = self.investor.evaluate(financial_statements)
        return evaluation

    # def store_all_possible_ticker_symbols(self, pages=None):
    #     for page in range(0, pages):
    #         ticker_set = self.polygon.get_polygon_ticker_symbols(pages=page, perpage=50)
    #         print(page, len(ticker_set), ticker_set)
    #         self._ticker_repo.post_many(ticker_set)

    # def store_financial_statement(self, symbol=None):
    #     if not symbol:
    #         return None
    #     financial_statement = polygon.get_polygon_financial_statement(symbol=symbol)
    #     return self._financial_statement_repo.post(financial_statement)

    # def _get_many_tickers(self, offset=None, limit=None):
    #     return self._ticker_repo.get_many(offset, limit)

    # def store_company_information_from_ticker_table(
    #     self, offset=0, limit=20, total=34277
    # ):
    #     offset = 9980
    #     while offset < total:
    #         print("the start:", offset)
    #         tickers = self._ticker_repo.get_many(offset=offset, limit=limit)
    #         company_details = []
    #         for ticker in tickers:
    #             company_detail = polygon.get_polygon_company_info(symbol=ticker.symbol)
    #             if company_detail:
    #                 company_details.append(company_detail)
    #         self._company_repo.post_many(company_details)
    #         offset += limit
    #     return

    # def store_financial_statement_from_ticker_table(
    #     self, offset=0, limit=100, total=34277
    # ):
    #     while offset < total:
    #         print("the start:", offset)
    #         tickers = self._ticker_repo.get_many(offset=offset, limit=limit)
    #         for ticker in tickers:
    #             fs_list = polygon.get_polygon_financial_statement(
    #                 symbol=ticker.symbol, limit=10
    #             )
    #             if fs_list:
    #                 self._financial_statement_repo.post_many(fs_list)
    #         offset += limit
    #         print(offset)
    #     return

    # def get_financial_statements(self, offset=0, limit=10):
    #     return self._financial_statement_repo.get(offset, limit)


# class TrackingUseCase:
#     def __init__(self):
#         self._alpaca_interface = AlpacaInterface()
#         self._polygon_interface = PolygonInterface()
#         watchlists = self._alpaca_interface.get_watchlists()
#         self.stocks_on_watchlists = []
#         for watchlist in watchlists:
#             watchlist_entity = self._alpaca_interface.get_watchlist(watchlist.id)
#             self.stocks_on_watchlists += watchlist_entity.assets

#     def _get_snapshot(self):
#         snapshot = self._polygon_interface.get_snapshot_of_tickers()

#         tickers = snapshot['tickers']

#         for stock in self.stocks_on_watchlists:
#             match = next((ticker for ticker in tickers if ticker['ticker'] == stock['symbol']), None)
#             print(match)

#     def _run_tracking_and_store_financial_data(self, wait_time_minutes):
#         tracking_job = Job(interval=timedelta(seconds=wait_time_minutes*60), execute=self._get_snapshot)
#         financial_statement_store_job = Job(interval=timedelta(seconds=1), execute=FinancialDataUseCase().store_financial_statement_from_ticker_table)
#         financial_statement_store_job.run()
#         tracking_job.run()

#         while True:
#             try:
#                 time.sleep(1)
#             except ProgramKilled:
#                 print("Program killed: running cleanup code")
#                 financial_statement_store_job.stop()
#                 break