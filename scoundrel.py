from deck import Deck


deck = Deck()
deck.shuffle()

for card in deck.cards:
    print(card)

# Draw a card
print("\nDrawn card:", deck.draw())


class Scoundrel:
    def __init__(self):
        pass
