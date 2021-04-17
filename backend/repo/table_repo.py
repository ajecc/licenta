from model.table import Table
from extensions import g_redis

class TableRepo:
    def __init__(self):
        pass
    
    def create_new(self):
        table = Table()
        table.update_to_redis()
        return table

    def get_by_id(self, id):
        return Table.from_redis(id)

    def remove(self, id):
        g_redis.remove_containing_id(id)
