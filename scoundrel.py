from deck import Deck


class Scoundrel:
    def __init__(self):
        self.deck = Deck()
        self.deck.prepare()
        self.deck.shuffle()
        self.discard = []

        self.health = 20

        self.current_room = []
        self.avoided_last_room = False
        self.draw_room()

    def avoid_room(self):
        if self.avoided_last_room:
            print("You cannot avoid two rooms in a row!")
            return

        print("===================================================")
        print("Avoiding the room...")

        self.deck.cards.extend(self.current_room)
        self.current_room = []
        self.draw_room()
        self.avoided_last_room = True

    def take_weapon(self):
        weapons = [card for card in self.current_room if card.suit in ["♦", "diamonds"]]

        if not weapons:
            print("No weapons available to take!")
            return

        if len(weapons) == 1:
            chosen_weapon = weapons[0]
        else:
            print("\nChoose a weapon to take:")
            for i, card in enumerate(weapons):
                print(f"  [{i+1}] {card}")
            choice = int(input("\nSelect a weapon: ")) - 1
            chosen_weapon = weapons[choice]

        print(f"You took the {chosen_weapon}!")
        self.current_room.remove(chosen_weapon)
        self.discard.append(chosen_weapon)  # You can change this if weapons should be stored elsewhere


    def fight(self):
        print("You fight a monster!")

    def heal(self):
        print("You drink a potion and heal!")

    def draw_room(self):
        num_cards = 4 - len(self.current_room)
        self.current_room = [self.deck.draw() for _ in range(num_cards)]

    def display_room(self):
        print(f"{len(self.deck.cards)}🂠 \t" + " ".join(map(str,
              self.current_room)) + f"\t{len(self.discard)}🂠")

        actions = self.get_available_actions()

        print("\nAvailable Actions:")
        for key, desc in actions.items():
            print(f"  [{key}] {desc}")

    def get_available_actions(self):
        actions = {}

        # monsters
        if any(card.suit in ["spades", "clubs"] for card in self.current_room):
            actions["F"] = "Fight a monster"

        # potions
        if any(card.suit == "hearts" for card in self.current_room):
            actions["H"] = "Heal with a potion"

        # weapons
        if any(card.suit == "diamonds" for card in self.current_room):
            actions["T"] = "Take a weapon"

        if not self.avoided_last_room:
            actions["A"] = "Avoid this room"

        actions["Q"] = "Quit the game"

        return actions

    def player_interaction(self):
        while True:
            self.display_room()
            actions = self.get_available_actions()

            choice = input("\nChoose an action: ").strip().upper()

            if choice in actions:
                if choice == "F":
                    self.fight_room()
                elif choice == "H":
                    self.heal()
                elif choice == "T":
                    self.take_weapon()
                elif choice == "A":
                    self.avoid_room()
                elif choice == "Q":
                    print("Thanks for playing!")
                    return
                break
            else:
                print("Invalid choice. Try again.")

    def __repr__(self):
        return f"{len(self.deck.cards)}🂠  - - - - {len(self.discard)}🂠"


game = Scoundrel()

while True:
    game.player_interaction()
