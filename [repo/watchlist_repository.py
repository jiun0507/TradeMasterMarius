from logging import exception
from alpaca_trade_api.entity import Watchlist
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
from models import WatchList


class WatchlistRepository:
    def __init__(self):
        self.engine = create_engine('sqlite:///financial_statement.db', echo=True)

    # could make into abstract function
    def get_or_create(session, defaults=None, **kwargs):
        instance = session.query(WatchList).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            params = dict((k, v) for k, v in kwargs.iteritems())
            params.update(defaults or {})
            instance = WatchList(**params)
            session.add(instance)
            return instance, True

    def get_all(self):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        watchlist = session.query(WatchList).all()
        formatted_watchlist = []
        for stock in watchlist:
            print(stock)
            formatted_stock = []
            formatted_stock.append(stock.symbol)
            formatted_stock.append(stock.expected_price)
            formatted_watchlist.append(formatted_stock)
        session.close()
        return formatted_watchlist

    def update_watchlist(self, stocks):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        print(stocks)
        try:
            for stock in stocks:
                instance = session.query(WatchList).filter_by(symbol=stock).first()
                if not instance:
                    session.add(
                        WatchList(symbol=stock),
                    )

            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def update_stock_on_watchlist(self, symbol, expected_price=0):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        instance = session.query(WatchList).filter_by(symbol=symbol).first()
        if instance:
            if expected_price == 0:
                return False
            else:
                instance.expectedPrice = expected_price
                session.commit()
        else:
            session.add(
                WatchList(
                    symbol=symbol,
                    expectedPrice=expected_price,
                )
            )
            session.commit()
        session.close()
        return True