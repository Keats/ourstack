import os

import yaml


def _validate_company(company_data):
    """
    A company should have at least a name, a website and 1 tech and a location
    key (even if location itself is not there)
    """
    stack = company_data.get('stack', [])

    has_techs = len(stack) > 1
    has_name = company_data.get('name') is not None
    # TODO: test validity of url ?
    has_website = company_data.get('website') is not None
    has_location = company_data.get('location') is not None

    return has_techs and has_name and has_website and has_location


def parse_directory(path):
    valid_companies = []

    for filename in os.listdir(path):
        fullpath = os.path.join(path, filename)

        if not os.path.isfile(fullpath):
            continue

        with open(fullpath, 'r') as file:
            company_data = yaml.safe_load(file.read())
            if _validate_company(company_data):
                valid_companies.append(company_data)
            else:
                print('File %s is not valid' % filename)

    return valid_companies
