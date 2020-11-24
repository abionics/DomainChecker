import csv
import os

from checker.db.database import Database
from checker.db.models import Domain, Base
from config import REPORTS_DIRECTORY


def create_report(query: str, filename: str = None):
    filename = __create_file(query, filename)
    keys = __get_table_keys(Domain)
    db = Database()
    results = db.session.query(Domain) \
        .filter_by(query=query, purchasable=True) \
        .order_by(Domain.purchase_price, Domain.renewal_price, Domain.tld) \
        .all()
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(keys)
        for result in results:
            row = [getattr(result, key) for key in keys]
            writer.writerow(row)


def __create_file(query: str, filename: str) -> str:
    if filename is None:
        filename = f'{query}.csv'
    filename = os.path.join(REPORTS_DIRECTORY, filename)
    os.makedirs(REPORTS_DIRECTORY, exist_ok=True)
    return filename


def __get_table_keys(table: Base) -> list:
    return table.__table__.columns.keys()
