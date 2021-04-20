import requests

class Request:
    def __init__(self):
        self.MAIN_URL = 'http://localhost:5000'
        self.session = requests.Session() 
        self.session.get(self.MAIN_URL)

    def login(self, username, password):
        request = self.session.post(f'{self.MAIN_URL}/auth/login', json={'username': username, 'password': password})
        return request.status_code, request.text 

    def register(self, email, username, password):
        request = self.session.post(f'{self.MAIN_URL}/auth/register', json={'email': email, 'username': username, 'password': password})
        return request.status_code, request.text

    def create_table(self, bots_cnt):
        request = self.session.post(f'{self.MAIN_URL}/create_table', json={'bots_cnt': bots_cnt})
        return request.status_code, request.text

    def join_table(self, table_code):
        request = self.session.post(f'{self.MAIN_URL}/join_table', json={'table_code': table_code})
        return request.status_code, request.text
    
    def get_game_state(self):
        request = self.session.get(f'{self.MAIN_URL}/game_state')
        return request.status_code, request.text
    
    def post_decision(self, decision_dict):
        request = self.session.post(f'{self.MAIN_URL}/decision', json=decision_dict)
        return request.status_code, request.text

    def leave_table(self):
        request = self.session.post(f'{self.MAIN_URL}/leave_table')
        return request.status_code, request.text


g_request = Request()
