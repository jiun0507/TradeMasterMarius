from alpaca_interface import PolygonInterface
from financial_statement_repository import FinancialStatementRepository
from ticker_repository import TickerRepository
from company_repository import CompanyRepository

polygon = PolygonInterface()

class FinancialDataUseCase:
    def __init__(self, repository) -> None:
        self._ticker_repo = TickerRepository()
        self._financial_statement_repo = FinancialStatementRepository()

    def store_all_possible_ticker_symbols(self, pages=None):
        for page in range(0, pages):
            ticker_set = polygon.get_polygon_ticker_symbols(page=page, perpage=50)
            self._ticker_repo.post_many(ticker_set)

    def store_financial_statement(self, symbol=None):
        if not symbol:
            return None
        financial_statement = polygon.get_polygon_financial_statement(symbol=symbol)
        return self._financial_statement_repo.post(financial_statement)

    def store_company_info(self, symbol=None):
        if not symbol:
            return None
        company_detail = polygon.get_polygon_company_info(symbol=symbol)
        return self._company_repo.post(company_detail)
