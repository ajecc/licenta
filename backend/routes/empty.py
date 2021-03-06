from flask import request, Response, Blueprint, session
from controller.controllers import table_controller, user_controller
from model.elem_bounds import UNIQ_CODE_LEN
from model.user import User
from extensions import g_redis
import game_process as gp

empty = Blueprint('empty', __name__)

@empty.route('/create_table', methods=['POST'])
def create_table():
    try:
        bots_cnt = int(request.json.get('bots_cnt'))
        if bots_cnt < 2 or bots_cnt > 5:
            raise ValueError()
    except:
        return Response('Number of bots must be between 2 and 5', status=400)
    table = table_controller.create_new(bots_cnt)
    if table is None:
        return Response('Could not create table', status=400)
    print(session.get('user_id'))
    user = user_controller.get_by_id(session.get('user_id'))
    if user is None:
        return Response('No user in this session', status=400)
    user = User(user.id)
    table_controller.remove_user_from_table(user)
    table.add_user(user)
    user.update_to_redis()
    gp.start_game(table.id)
    return Response('', status=200)


@empty.route('/join_table', methods=['POST'])
def join_table():
    table_code = request.json.get('table_code') 
    if table_code is None or len(table_code) != UNIQ_CODE_LEN:
        return Response('Invalid table code', status=400)
    table = table_controller.get_by_id(table_code)
    if table is None:
        return Response('No such table', status=400)
    user = user_controller.get_by_id(session.get('user_id'))
    if user is None:
        return Response('No user in this session', status=400)
    if len(table.current_users_ids) >= 6:
        return Response('Table if full', status=400)
    table_controller.remove_user_from_table(user)
    table.add_user(user)
    return Response('', status=200)


@empty.route('/game_state', methods=['GET'])
def get_game_state():
    user = user_controller.get_by_id(session.get('user_id'))
    if user is None:
        return Response('No user in this session', status=400)
    if user.table_id is None:
        return Response('User didn\'t join a table', status=400)
    state_json = g_redis.get_raw(f'game#{user.table_id}#{user.id}')
    return Response(
            response=state_json,
            status=200,
            mimetype='application/json')


@empty.route('/decision', methods=['POST'])
def post_decision():
    user = user_controller.get_by_id(session.get('user_id'))
    if user is None:
        return Response('No user in this session', status=400)
    if user.table_id is None:
        return Response('User didn\'t join a table', status=400)
    g_redis.set(user.id, 'user:decision', str(request.json))
    return Response('', status=200)


@empty.route('/leave_table', methods=['POST'])
def leave_table():
    user = user_controller.get_by_id(session.get('user_id'))
    if user is None:
        return Response('No user in this session', status=400)
    if user.table_id is None:
        return Response('User didn\'t join a table', status=400)
    table_controller.remove_user_from_table(user)
    return Response('', status=200)

