from repo.cred_repo import CredRepo 
from model.cred import Cred
from flask import Response
from passlib.hash import pbkdf2_sha256
import re
from model.elem_bounds import EMAIL_LEN, USERNAME_LEN, PASSWORD_MIN_LEN, PASSWORD_MAX_LEN


class CredController:
    def __init__(self, user_controller):
        self.repo = CredRepo() 
        self._user_controller = user_controller

    def add(self, email, username, password):
        status, reason = self._validate_email(email)
        if not status:
            return Response(reason, status=400)
        status, reason = self._validate_username(username)
        if not status:
            return Response(reason, status=400)
        status, reason = self._validate_password(password)
        if not status:
            return Response(reason, status=400)
        password_hash = pbkdf2_sha256.hash(password)
        cred = Cred(email, username, password_hash)
        self.repo.add(cred)
        self._user_controller.create_new(cred.id) 
        return Response('OK', status=200)

    def check(self, email, username, password):
        if self.repo.check(email, username, password):
            return Response('OK', status=200)
        return Response('Invalid credentials', status=400)

    def get_by_id(self, id):
        return self.repo.get_by_id(id)

    def get_by_username(self, username):
        return self.repo.get_by_username(username)

    def bet_by_email(self, email):
        return self.repo.get_by_email(email)

    def _validate_email(self, email):
        if email is None:
            return False, "No email"
        if len(email) >= EMAIL_LEN:
            return False, 'Email too long'
        if not re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
            return False, 'Invalid email format'
        if self.repo.contains_email(email):
            return False, 'Email already registered'
        return True, ''

    def _validate_username(self, username):
        if username is None:
            return False, 'No username'
        if len(username) >= USERNAME_LEN:
            return False, 'Username too long'
        if not username.isalnum():
            return False, 'Username is not alphanumeric'
        if self.repo.contains_username(username):
            return False, 'Username already exists'
        return True, ''

    def _validate_password(self, password):
        if password is None:
            return False, 'No password'
        if len(password) < PASSWORD_MIN_LEN:
            return False, 'Password too short'
        if len(password) > PASSWORD_MAX_LEN:
            return False, 'Password too long'
        if len(password) != len(password.strip()):
            return False, 'The password can\'t contain spaces'
        if re.search(r'\d', password) is None:
            return False, 'The password must contain at least a digit'
        if re.search(r'[A-Z]', password) is None:
            return False, 'The password must contain at least an upper case letter'
        if re.search(r'[a-z]', password) is None:
            return False, 'The password must contain at least a lowercase case letter'
        if re.search(r'\W', password) is None:
            return False, 'The password must contain at least a special symbol'
        return True, ''





