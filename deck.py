import random
from card import Card


class Deck:
    RED_SUITS = {'hearts', 'diamonds'}
    BLACK_SUITS = {'clubs', 'spades'}

    def __init__(self, empty=False):
        self.cards = [] if empty else self._generate_deck()

    def _generate_deck(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop(0) if self.cards else None

    def prepare(self):
        self.cards = [
            card for card in self.cards
            if not (card.suit in self.RED_SUITS and card.value >= 11)
        ]

    def __repr__(self):
        rows = [", ".join(map(str, self.cards[i:i+13])) for i in range(0, len(self.cards), 13)]
        return f"Deck({len(self.cards)} cards)\n" + "\n".join(rows)
