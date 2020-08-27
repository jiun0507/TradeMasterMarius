from requests.sessions import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
from models import DBSession


class TickerRepository:
    def __init__(self):
        self.engine = create_engine('sqlite:///financial_statement.db', echo=True)

    def post_many(self, tickers):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        try:
            with session.no_autoflush:
                for ticker in tickers:
                    if ticker.get('ticker', None):
                        ticker_instance = models.Ticker(
                            symbol=ticker['ticker'],
                        )
                        session.add(ticker_instance)
            session.commit()
            print("Post successful.")
        except Exception as e:
            print("Post many failed. Roll Back ! ", e)
            session.rollback()
        finally:
            session.close()

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
        return session.query(models.Ticker).offset(offset).limit(limit).all()


    def get(self, symbol):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        ticker = session.query(models.Ticker).get(symbol=symbol)
        return ticker