from model.table import Table
from model.cred import Cred
from model.user import User
from extensions import g_redis

class TableRepo:
    def __init__(self):
        pass
    
    def create_new(self, bots_cnt):
        table = Table(bots_cnt)
        for i in range(bots_cnt):
            bot_cred = Cred('', f'bot_{i}')
            bot_user = User(bot_cred.id)
            bot_user.is_bot = True
            bot_cred.update_to_redis()
            table.add_user(bot_user)
            bot_user.update_to_redis()
        table.update_to_redis()
        return table

    def get_by_id(self, id):
        return Table.from_redis(id)

    def remove(self, id):
        g_redis.remove_containing_id(id)
