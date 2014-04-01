import sys

from models import Company, Tech, Location, setup_db
from parser import parse_directory


def load_company(session, company_data):
    company = Company(
        name=company_data.get('name'),
        website=company_data.get('website'),
        description=company_data.get('description'),
        size=company_data.get('size'),
        remote=company_data.get('allows_remote')
    )
    company.techs = [Tech(name=tech_name) for tech_name in company_data.get('stack', [])]

    company.location = Location(
        city=company_data['location'].get('city'),
        country=company_data['location'].get('country'),
        postcode=company_data['location'].get('postcode')
    )

    session.add(company)
    session.commit()


if __name__ == "__main__":
    db_url = 'postgresql://testing:password@localhost/ourstack'
    companies_path = '../companies'

    # allows specifying the db url when calling the script directly
    if len(sys.argv) > 1:
        db_url = sys.argv[1]

    session = setup_db(db_url)

    for company_data in parse_directory(companies_path):
        load_company(session, company_data)

    for instance in session.query(Company):
        print(instance.name)
