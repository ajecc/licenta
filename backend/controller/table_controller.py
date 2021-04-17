from repo.table_repo import TableRepo
from controller.controllers import user_controller


class TableController:
    def __init__(self):
        self._repo = TableRepo()

    def create_new(self):
        return self._repo.create_new()

    def get_by_id(self, id):
        return self._repo.get_by_id(id)

    def remove_user_from_table(self, user):
        table = self.get_by_id(user.table_id)
        table.remove_user_from_table(user)

    def remove_table(self, table_id):
        table = self._repo.get_by_id(table_id)
        for user_id in table.current_users_ids:
            user = user_controller.get_by_id(user_id) 
            table.remove_user(user)
            if user.is_bot:
                user_controller.remove(user.id)
        self.remove(table_id)

    def remove(self, table_id):
        self._repo.remove(table_id)
