from flask import request, Response, Blueprint, session
from controller.controllers import table_controller, user_controller
from model.elem_bounds import UNIQ_CODE_LEN

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
    table.add_user(user)

@empty.route('/join_table', methods=['POST'])
def join_table():
    table_code = request.json.get('table_code') 
    if table_code is None or len(table_code) != UNIQ_CODE_LEN:
        return Response(400, 'Invalid table code')
    table = table_code.get_by_uniq_code(table_code)
    if table is None:
        return Response(400, 'No such table')
    user = user_controller.get_by_id(session.get('user_id'))
    if user is None:
        return Response(500, 'No user in this session')
    table.add_user(user)

