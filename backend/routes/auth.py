from flask import request, Response, Blueprint, session
from controller.controllers import cred_controller, user_controller

auth = Blueprint('auth', __name__)


@auth.route('/auth/register', methods=['POST'])
def register():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    response = cred_controller.add(email, username, password)
    if response.status != 200:
        return response
    user_controller.create_new(cred_controller.get_by_username(username).id)
    return response


@auth.route('/auth/login', methods=['POST'])
def login():
    if 'user_id' in session:
        return Response(f'Logged in as {session["user_id"]}', status=200)
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    response = cred_controller.check(email, username, password)
    if response.status != 200:
        return response
    user = cred_controller.get_by_username(username)
    if user is None:
        user = cred_controller.get_by_email(email)
    session['user_id'] = user.id
    return response
