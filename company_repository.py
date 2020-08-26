from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models


class TickerRepository:
    def __init__(self):
        self.engine = create_engine('sqlite:///financial_statement.db', echo=True)

    def post(self, company_detail):
        if not company_detail:
            return None

        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

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


    def create_company_informations(self, company_details):
        if len(company_details) > 100:
            print('This is too much information to load.')
            return None
        if not company_details or len(company_details) == 0:
            print('There is no information.')
            return None
        post_body = []
        for company_detail in company_details:
            post_body.append(
                (
                    company_detail.get('symbol', None),
                    company_detail.get('logo', None),
                    company_detail.get('exchange', None),
                    company_detail.get('name', None),
                    company_detail.get('cik', None),
                    company_detail.get('bloomberg', None),
                    company_detail.get('lei', None),
                    company_detail.get('sic', None),
                    company_detail.get('country', None),
                    company_detail.get('industry', None),
                    company_detail.get('sector', None),
                    company_detail.get('marketcap', None),
                    company_detail.get('employees', None),
                    company_detail.get('phone', None),
                    company_detail.get('ceo', None),
                    company_detail.get('url', None),
                    company_detail.get('description', None),
                ),
            )
