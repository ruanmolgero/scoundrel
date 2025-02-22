class Card:
    suit_symbols = {
        'hearts': ('♥', '\033[31m'),
        'diamonds': ('♦', '\033[31m'),
        'clubs': ('♣', '\033[32m'),
        'spades': ('♠', '\033[32m')
    }

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        symbol, color = self.suit_symbols[self.suit]
        return f"{color}{self.rank}{symbol}\033[0m"
