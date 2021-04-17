import json


class Decision:
    FOLD = 'FOLD'
    CHECK = 'CHECK'
    CALL = 'CALL'
    BET = 'BET'

    DECISION_TIME = 20  # seconds

    def __init__(self, decision, bet_ammount=None):
        self._decision = decision
        self._bet_ammount = bet_ammount

    def __eq__(self, other):
        return self._decision == other.decision

    def to_json(self):
        json_ = {}
        json_['decision'] = self._decision
        json_['bet_ammount'] = self._bet_ammount
        return json.dumps(json_)

    @property
    def decision(self):
        return self._decision

    @classmethod
    def from_json(cls, decision_json):
        if decision_json is None:
            return None
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
