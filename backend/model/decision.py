import json


class Decision:
    FOLD = 'FOLD'
    CHECK = 'CHECK'
    CALL = 'CALL'
    BET = 'BET'

    def __init__(self, decision, bet_ammount=None):
        self._decision = decision
        self._bet_ammount = bet_ammount

    @classmethod
    def from_json(cls, decision_json):
        loaded = json.loads('decision_json')
        if 'decision' not in loaded.keys():
            raise ValueError('Decision json has to contain "decision"')
        decision = loaded['decision']
        if decision == Decision.BET:
            if 'bet_ammount' not in loaded.keys():
                raise ValueError('Decision json with BET has to contain "bet_ammount"') 
            try:
                bet_ammount = int(loaded['bet_ammount'])
            except:
                raise ValueError('"bet_ammount" in decision json has to be an integer')
        return cls(decision, bet_ammount)
