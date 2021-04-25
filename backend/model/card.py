import secrets
import pokereval.card


class Card:
    COLORS = ['s', 'h', 'c', 'd']
    COLORS_IND = {c: i + 1 for i, c in enumerate(COLORS)} 
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    RANKS_IND = {r: i + 2 for i, r in enumerate(RANKS)} 

    def __init__(self, rank_color=None, color=None):
        if color is not None:
            self._rank = rank_color
            self._color = color 
        else:
            self._rank = rank_color[0]
            self._color = rank_color[1]

    def to_pokereval(self):
        return pokereval.card.Card(Card.RANKS_IND[self._rank], Card.COLORS_IND[self._color])

    def __str__(self):
        return self._rank + self._color


__ALL_CARDS = [Card(r, c) for r in Card.RANKS for c in Card.COLORS]
__CARDS_SELECTOR = secrets.SystemRandom()

def generate_random(used_cards):
    available_cards = list(filter(lambda c: c not in used_cards, __ALL_CARDS))
    return __CARDS_SELECTOR.sample(available_cards, 1)[0]
