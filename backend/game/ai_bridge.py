import ctypes
import os
import json
from model.decision import Decision

class AiBridge:
    def __init__(self):
        os.chdir('ai')
        os.add_dll_directory(os.getcwd())
        user_dll = ctypes.WinDLL('ai.dll')
        process_query_proto = ctypes.WINFUNCTYPE(ctypes.c_double, ctypes.c_char_p)
        update_symbols_proto = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        process_query_params = (1, 'pquery', 0),
        update_symbols_params = (1, 'psymbols', 0),
        self._process_query = process_query_proto(('process_query', user_dll), process_query_params)
        self._update_symbols = update_symbols_proto(('update_symbols', user_dll), update_symbols_params)

    def get_decision(self, symbols_json):
        self._update_symbols_wrapper(self._convert_to_dll_symbols(symbols_json))
        self._process_query_wrapper('dll$beep')
        sum = self._process_query_wrapper('dll$betsize')
        EPS = 0.1
        if abs(self._process_query_wrapper('dll$check') - 1) < EPS:
            return Decision(Decision.CHECK)
        elif abs(self._process_query_wrapper('dll$call') - 1) < EPS:
            return Decision(Decision.CALL)
        elif abs(self._process_query_wrapper('dll$bet') - 1) < EPS:
            sum = int(sum + EPS)
            return Decision(Decision.BET, sum)
        return Decision(Decision.FOLD)

    def _process_query_wrapper(self, query):
        return self._process_query(ctypes.c_char_p(query.encode()))

    def _update_symbols_wrapper(self, symbols):
        return self._update_symbols(ctypes.c_char_p(symbols.encode()))
    
    def _convert_to_dll_symbols(self, symbols_json):
        symbols = json.loads(symbols_json)
        dll_symbols = ''
        for i in range(5):
            card = 'nocard'
            if len(symbols['board']['cards']) > i:
                card = symbols['board']['cards'][i]
            dll_symbols += f'c0cardface{i}:{card}\n'
        dll_symbols += f'c0pot0:{symbols["board"]["pot"]}\n'
        dll_symbols += 'c0pot1:0\n'
        users = symbols['users']
        # TODO: handle heads-up
        main_name = users[2]['name']
        users = users[::-1]
        while users[2]['name'] != main_name:
            temp = users[0]
            users = users[1:]
            users.append(temp)
        for i, user in enumerate(users):
            if len(user['cards']) != 0:
                temp = 1
            else:
                temp = 0
            dll_symbols += f'p{i}active:{temp}\n'
            dll_symbols += f'p{i}balance:{user["balance"]}\n'
            dll_symbols += f'p{i}bet:{user["bet"]}\n'
            if i == 2:
                dll_symbols += f'p{i}cardface0:{user["cards"][0]}\n'
                dll_symbols += f'p{i}cardface1:{user["cards"][1]}\n'
            dll_symbols += f'p{i}dealer:{int(user["dealer"])}\n'
            dll_symbols += f'p{i}name:{user["name"]}\n'
            dll_symbols += f'p{i}seated:{int(user["seated"])}\n'
        dll_symbols += f'bblind:{symbols["board"]["bb"]}'
        return dll_symbols
