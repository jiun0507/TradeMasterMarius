from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models


class FinancialStatementRepository:
    def __init__(self):
        self.engine = create_engine('sqlite:///financial_statement.db', echo=True)

    def post(self, fs):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        try:
            financial_statement = models.FinancialStatement(
                None,
                fs.get('data_source', 'polygon'),
                fs.get('ticker', None),
                fs.get('period', None),
                fs.get('calendarDate', None),
                fs.get('reportPeriod', None),
                fs.get('updated', None),
            )
            financial_statement_vi = models.FinancialStatementValueInvestment(
                None,
                financial_statement.id,
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

            session.add(financial_statement)
            session.add(financial_statement_vi)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def post_many(self, fs_list):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        try:
            for fs in fs_list:
                if not fs:
                    continue
                try:
                    financial_statement = models.FinancialStatement(
                        dataSource=fs.get('data_source', 'polygon'),
                        symbol=fs.get('ticker', None),
                        period=fs.get('period', None),
                        calendarDate=fs.get('calendarDate', None),
                        reportPeriod=fs.get('reportPeriod', None),
                        updated=fs.get('updated', None),
                    )
                    financial_statement_vi = models.FinancialStatementValueInvestment(
                        enterpriseValue=fs.get('enterpriseValue', None),
                        enterpriseValueOverEBIT=fs.get('enterpriseValueOverEBIT', None),
                        enterpriseValueOverEBITDA=fs.get('enterpriseValueOverEBITDA', None),
                        payoutRatio=fs.get('payoutRatio', None),
                        priceToBookValue=fs.get('priceToBookValue', None),
                        priceEarnings=fs.get('priceEarnings', None),
                        priceToEarnings=fs.get('priceToEarnings', None),
                        priceToEarningsRatio=fs.get('priceToEarningsRatio', None),
                        preferredDividendsIncomeStatementImpact=fs.get('preferredDividendsIncomeStatementImpact', None),
                        sharePriceAdjustedClose=fs.get('sharePriceAdjustedClose', None),
                        priceSales=fs.get('priceSales', None),
                        priceToSalesRatio=fs.get('priceToSalesRatio', None),
                        returnOnAverageAssets=fs.get('returnOnAverageAssets', None),
                        returnOnAverageEquity=fs.get('returnOnAverageEquity', None),
                        returnOnInvestedCapital=fs.get('returnOnInvestedCapital', None),
                        returnOnSales=fs.get('returnOnSales', None),
                        shares=fs.get('shares', None),
                        weightedAverageShares=fs.get('weightedAverageShares', None),
                        weightedAverageSharesDiluted=fs.get('weightedAverageSharesDiluted', None),
                        salesPerShare=fs.get('salesPerShare', None),
                        tangibleAssetsBookValuePerShare=fs.get('tangibleAssetsBookValuePerShare', None),
                    )
                    financial_statement.financial_statement_value_investment = financial_statement_vi
                    session.add(financial_statement)
                except Exception as e:
                    print('Financial Statement not added: ', e)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
