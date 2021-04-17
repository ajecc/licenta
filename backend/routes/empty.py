from flask import request, Response, Blueprint, session
from controller.controllers import table_controller, user_controller
from model.elem_bounds import UNIQ_CODE_LEN
from extensions import g_redis
import game.game_process as gp

empty = Blueprint('empty', __name__)

@empty.route('/create_table', methods=['POST'])
def create_table():
    try:
        bots_cnt = int(request.json.get('bots_cnt'))
        if bots_cnt < 1 or bots_cnt > 5:
            raise ValueError()
    except:
        return Response(400, 'Invalid number of bots')
    table = table_controller.create_table(bots_cnt)
    if table is None:
        return Response(500, 'Could not create table')
    user = user_controller.get_by_id(session.get('user_id'))
    if user is None:
        return Response(500, 'No user in this session')
    table_controller.remove_user_from_table(user)
    table.add_user(user)
    gp.start_game(table.id)
    return Response(200)


@empty.route('/join_table', methods=['POST'])
def join_table():
    table_code = request.json.get('table_code') 
    if table_code is None or len(table_code) != UNIQ_CODE_LEN:
        return Response(400, 'Invalid table code')
    table = table_controller.get_by_id(table_code)
    if table is None:
        return Response(400, 'No such table')
    user = user_controller.get_by_id(session.get('user_id'))
    if user is None:
        return Response(500, 'No user in this session')
    if len(table.current_users_ids) >= 6:
        return Response(400, 'Table if full')
    table_controller.remove_user_from_table(user)
    table.add_user(user)
    return Response(200)


@empty.route('/game_state', methods=['GET'])
def get_game_state():
    user = user_controller.get_by_id(session.get('user_id'))
    if user is None:
        return Response(500, 'No user in this session')
    if user.table_id is None:
        return Response(400, 'User didn\'t join a table')
    state_json = g_redis.get_raw(f'game#{user.table_id}#{user.id}')
    response = empty.response_class(
            response=state_json,
            status=200,
            mimetype='application/json')
    return response


@empty.route('/decision', methods=['POST'])
def post_decision():
    user = user_controller.get_by_id(session.get('user_id'))
    if user is None:
        return Response(500, 'No user in this session')
    if user.table_id is None:
        return Response(400, 'User didn\'t join a table')
    g_redis.set(user.id, 'user:decision', str(request.json))
    return Response(200)


@empty.route('/leave_table', methods=['POST'])
def leave_table():
    user = user_controller.get_by_id(session.get('user_id'))
    if user is None:
        return Response(500, 'No user in this session')
    if user.table_id is None:
        return Response(400, 'User didn\'t join a table')
    table_controller.remove_user_from_table(user)
    return Response(200)

