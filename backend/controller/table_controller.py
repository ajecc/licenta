from repo.table_repo import TableRepo


class TableController:
    def __init__(self):
        self._repo = TableRepo()

    def create_new(self):
        return self._repo.create_new()

    def get_by_uniq_code(self, uniq_code):
        return self._repo.get_by_uniq_code(uniq_code)



