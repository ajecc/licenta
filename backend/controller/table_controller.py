from repo.table_repo import TableRepo


class TableController:
    def __init__(self, user_controller):
        self._repo = TableRepo()
        self._user_controller = user_controller

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
            user = self._user_controller.get_by_id(user_id) 
            table.remove_user(user)
            if user.is_bot:
                self._user_controller.remove(user.id)
        self.remove(table_id)

    def remove(self, table_id):
        self._repo.remove(table_id)
