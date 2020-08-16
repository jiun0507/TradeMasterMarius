class AlpacaUseCase:
    def __init__(self, repository) -> None:
        self._repo = repository
    def get(self):
        return self._repo.get_account_info()

    def get_financial_statement(self, symbol=None):
        return self._repo.get_polygon_financial_statement(symbol=symbol, limit=1)

    def get_positions(self):
        return self._repo.get_position_list()

    def update_ticker_symbols(self):
        return self._repo.get_polygon_supported_ticker_symbols(700)