from extensions import db
from model.table import Table

class TableRepo:
    def __init__(self):
        pass
    
    def create_new(self):
        table = Table()
        db.session.add(table)
        db.session.commit()
        return table

    def get_by_uniq_code(self, uniq_code):
        return Table.query.filter_by(uniq_code=uniq_code)
