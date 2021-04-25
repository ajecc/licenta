import requests
import socket

class Request:
    def __init__(self):
        host = socket.gethostbyname('localhost')
        self._MAIN_URL = f'http://{host}:5000'
        self._session = requests.Session() 
        self._session.get(self._MAIN_URL)

    def login(self, username, password):
        request = self._session.post(f'{self._MAIN_URL}/auth/login', json={'username': username, 'password': password})
        return request.status_code, request.text 

    def register(self, email, username, password):
        request = self._session.post(f'{self._MAIN_URL}/auth/register', json={'email': email, 'username': username, 'password': password})
        return request.status_code, request.text

    def create_table(self, bots_cnt):
        request = self._session.post(f'{self._MAIN_URL}/create_table', json={'bots_cnt': bots_cnt})
        return request.status_code, request.text

    def join_table(self, table_code):
        request = self._session.post(f'{self._MAIN_URL}/join_table', json={'table_code': table_code})
        return request.status_code, request.text
    
    def get_game_state(self):
        request = self._session.get(f'{self._MAIN_URL}/game_state')
        return request.status_code, request.text
    
    def post_decision(self, decision_dict):
        request = self._session.post(f'{self._MAIN_URL}/decision', json=decision_dict)
        return request.status_code, request.text

    def leave_table(self):
        request = self._session.post(f'{self._MAIN_URL}/leave_table')
        return request.status_code, request.text


g_request = Request()
