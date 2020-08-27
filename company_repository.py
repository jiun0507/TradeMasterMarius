from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models


class CompanyRepository:
    def __init__(self):
        self.engine = create_engine('sqlite:///financial_statement.db', echo=True)

    def post(self, company_detail):
        if not company_detail:
            return None
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        try:
            company = models.Company(
                company_detail['symbol'],
                company_detail['logo'],
                company_detail['exchange'],
                company_detail['name'],
                company_detail['cik'],
                company_detail['bloomberg'],
                company_detail['lei'],
                company_detail['sic'],
                company_detail['country'],
                company_detail['industry'],
                company_detail['sector'],
                company_detail['marketcap'],
                company_detail['employees'],
                company_detail['phone'],
                company_detail['ceo'],
                company_detail['url'],
                company_detail['description'],
            )
            session.add(company)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def post_many(self, company_details):
        if len(company_details) > 100:
            print('This is too much information to load.')
            return None
        if not company_details or len(company_details) == 0:
            print('There is no information.')
            return None

        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        try:
            for company_detail in company_details:
                with session.no_autoflush:
                    try:
                        company = models.Company(
                            symbol=company_detail.get('symbol', None),
                            logo=company_detail.get('logo', None),
                            exchange=company_detail.get('exchange', None),
                            name=company_detail.get('name', None),
                            cik=company_detail.get('cik', None),
                            bloomberg=company_detail.get('bloomberg', None),
                            lei=company_detail.get('lei', None),
                            sic=company_detail.get('sic', None),
                            country=company_detail.get('country', None),
                            industry=company_detail.get('industry', None),
                            sector=company_detail.get('sector', None),
                            marketCap=company_detail.get('marketcap', None),
                            employees=company_detail.get('employees', None),
                            phone=company_detail.get('phone', None),
                            ceo=company_detail.get('ceo', None),
                            url=company_detail.get('url', None),
                            description=company_detail.get('description', None),
                        )
                        session.add(company)
                    except Exception as e:
                        print("company not added", e)
            session.commit()
        except Exception as e:
            print("Roll Back! ", e)
            session.rollback()
        finally:
            session.close()
