from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
from models import WatchList


class WatchlistRepository:
    def __init__(self):
        self.engine = create_engine('sqlite:///financial_statement.db', echo=True)

    def get_all(self):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        watchlist = session.query(WatchList).filter()
        formatted_watchlist = []
        print(len(formatted_watchlist))
        for stock in watchlist:
            print(stock)
            formatted_stock = []
            formatted_stock.append(stock.symbol)
            formatted_stock.append(stock.expected_price)
            formatted_watchlist.append(formatted_stock)
        session.close()
        return formatted_watchlist
