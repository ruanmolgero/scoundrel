class Card:
    suit_symbols = {
        'hearts': ('♥', '\033[31m'),
        'diamonds': ('♦', '\033[31m'),
        'clubs': ('♣', '\033[32m'),
        'spades': ('♠', '\033[32m')
    }

    face_values = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.value = int(self.rank) if self.rank.isnumeric() else self.face_values[self.rank]
        self.suit = suit

    def __repr__(self):
        symbol, color = self.suit_symbols[self.suit]
        return f"{color}{self.rank}{symbol}\033[0m"
