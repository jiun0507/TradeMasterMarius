from requests.sessions import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
from models import DBSession


class TickerRepository:
    def __init__(self):
        self.engine = create_engine('sqlite:///financial_statement.db', echo=True)

    def post(self, ticker):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        try:
            ticker_instance = models.Ticker(
                symbol=ticker['symbol'],
            )
            session.add(ticker_instance)
            session.commit()
        except:
            session.rollback()
        finally:
            sesssion.close()


    def get_many(self, limit=None, offset=None):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query('Ticker')

        if offset:
            query.offset(offset)

        if limit:
            query.limit(limit)
        return query

    def get(self, symbol):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        ticker = session.query('Ticker').get(symbol=symbol)
        return ticker