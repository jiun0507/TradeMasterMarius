from Interface import PolygonInterface


class PolygonGateway:
    def __init__(self, accountant):
        self.polygon = PolygonInterface(accountant)

    def get_polygon_financial_statement(self, symbol, limit):
        results = self.polygon.get_polygon_financial_statement(symbol, limit)
        return results
