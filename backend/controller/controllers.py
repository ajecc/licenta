from controller.cred_controller import CredController
from controller.user_controller import UserController
from controller.table_controller import TableController

user_controller = UserController()
cred_controller = CredController(user_controller)
table_controller = TableController(user_controller)
