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


    def get(self, limit=None, offset=None):
        query = Query.from_('Tickers').select('*')
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return self.db.get(str(query))

