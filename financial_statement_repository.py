from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models


class TickerRepository:
    def __init__(self):
        self.engine = create_engine('sqlite:///financial_statement.db', echo=True)

    def post(self, ticker):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        ticker_instance = models.Ticker(
            symbol=ticker['symbol'],
        )
        session.add(ticker_instance)
        session.commit()

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
