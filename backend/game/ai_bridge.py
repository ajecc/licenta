import ctypes
import os
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
        self._update_symbols(symbols_json)
        self._process_query('dll$beep')
        sum = self._process_query('dll$betsize')
        EPS = 0.1
        if abs(self._process_query('dll$check') - 1) < EPS:
            return Decision(Decision.CHECK)
        elif abs(self._process_query('dll$call') - 1) < EPS:
            return Decision(Decision.CALL)
        elif abs(self._process_query('dll$bet') - 1) < EPS:
            sum = int(sum + EPS)
            return Decision(Decision.BET, sum)
        return Decision(Decision.FOLD)

    def _process_query(self, query):
        return self._process_query(ctypes.c_char_p(query.encode()))

    def _update_symbols(self, symbols_json):
        return self._update_symbols(ctypes.c_char_p(symbols_json.encode()))

