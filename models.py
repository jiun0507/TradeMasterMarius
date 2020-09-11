from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


engine = create_engine('sqlite:///financial_statement.db', echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base = declarative_base()


class WatchList(Base):
    __tablename__ = 'watchlist'
    id = Column(Integer, primary_key=True)

    symbol = Column(String, unique=True)
    watchlist_id = Column(String)
    expected_price = Column(Integer)
    def __repr__(self):
       return "<WatchList(symbol='%s'>" % (
                               self.symbol)


class Ticker(Base):
    __tablename__ = 'ticker'

    # Every SQLAlchemy table should have a primary key named 'id'
    id = Column(Integer, primary_key=True)

    symbol = Column(String, unique=True)

    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<Ticker(symbol='%s'>" % (
                               self.symbol)

class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    logo = Column(String)
    exchange = Column(String)
    name = Column(String)
    cik = Column(String)
    bloomberg = Column(String)
    lei = Column(String)
    sic = Column(Integer)
    country = Column(String)
    industry = Column(String)
    sector = Column(String)
    marketCap = Column(String)
    employees = Column(String)
    phone = Column(String)
    ceo = Column(String)
    url = Column(String)
    description = Column(String)

    def __repr__(self):
       return "<Company(symbol='%s'>" % (
                               self.symbol)

class FinancialStatement(Base):
    __tablename__ = 'financial_statement'

    id = Column(Integer, primary_key=True)
    dataSource = Column(String)
    symbol = Column(String)
    period = Column(String)
    calendarDate = Column(String)
    reportPeriod = Column(String)
    updated = Column(String)
    UniqueConstraint(symbol, period, calendarDate, reportPeriod)
    financial_statement_value_investment = relationship('FinancialStatementValueInvestment', back_populates='financial_statement', uselist=False)

class FinancialStatementValueInvestment(Base):
    __tablename__ = 'financial_statement_value_investment'

    id = Column(Integer, primary_key=True)
    financial_statement_id = Column(Integer, ForeignKey('financial_statement.id'))
    financial_statement = relationship("FinancialStatement", back_populates="financial_statement_value_investment")
    enterpriseValue = Column(Integer)
    enterpriseValueOverEBIT = Column(Integer)
    enterpriseValueOverEBITDA = Column(Integer)
    payoutRatio = Column(Integer)
    priceToBookValue = Column(Integer)
    priceEarnings = Column(Integer)
    priceToEarnings = Column(Integer)
    priceToEarningsRatio = Column(Integer)
    preferredDividendsIncomeStatementImpact = Column(Integer)
    sharePriceAdjustedClose = Column(Integer)
    priceSales = Column(Integer)
    priceToSalesRatio = Column(Integer)
    returnOnAverageAssets = Column(Integer)
    returnOnAverageEquity = Column(Integer)
    returnOnInvestedCapital = Column(Integer)
    returnOnSales = Column(Integer)
    shares = Column(Integer)
    weightedAverageShares = Column(Integer)
    weightedAverageSharesDiluted = Column(Integer)
    salesPerShare = Column(Integer)
    tangibleAssetsBookValuePerShare = Column(Integer)

# Create all tables by issuing CREATE TABLE commands to the DB.
Base.metadata.create_all(engine)