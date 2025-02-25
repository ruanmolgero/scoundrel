import os
from card import Card
from deck import Deck
from typing import List


def clear_screen():
    # Windows -> cls, Linux/Mac -> clear
    os.system("cls" if os.name == "nt" else "clear")


class Scoundrel:
    def __init__(self):
        self.deck = Deck()
        self.deck.prepare()
        self.deck.shuffle()
        self.discard = []

        self.health = 20
        self.weapon: Card = None
        self.weapon_kills: List[Card] = []

        self.current_room = []

        self.healed_this_turn = False
        self.avoided_last_room = False
        self.last_action = ""
        self.draw_room()

    def draw_room(self):
        num_cards = min(4 - len(self.current_room), len(self.deck.cards))
        for _ in range(num_cards):
            self.current_room.append(self.deck.draw())

    def display_room(self):
        clear_screen()
        tab_count = 2 if len(self.current_room) <= 2 else 1
        tabs = "\t" * tab_count

        print(f"{len(self.deck.cards)}🂠 \t" + " ".join(map(str, self.current_room)) + f"{tabs}{len(self.discard)}🂠")
        print(f"Health: {self.health}")
        print(f"Weapon: {self.weapon} | " + " ".join(map(str, self.weapon_kills)))

    def get_player_action(self):
        actions = self.get_available_actions()

        print("\nAvailable Actions:")
        for key, desc in actions.items():
            print(f"  [{key}] {desc}")

        while True:
            choice = input("\nChoose an action: ").strip().upper()
            if choice in actions:
                return choice
            else:
                print("Invalid choice. Try again.")

    def get_available_actions(self):
        actions = {}

        monsters = [card for card in self.current_room if card.suit in ["spades", "clubs"]]
        potions = [card for card in self.current_room if card.suit in ["hearts"]]
        weapons = [card for card in self.current_room if card.suit in ["diamonds"]]

        for i, monster in enumerate(monsters):
            actions[f"F{i+1}"] = f"Fight {monster}"

        for i, potion in enumerate(potions):
            actions[f"H{i+1}"] = f"Use {potion}"

        for i, weapon in enumerate(weapons):
            actions[f"T{i+1}"] = f"Take {weapon}"

        if len(self.current_room) == 4 and not self.avoided_last_room:
            actions["A"] = "Avoid this room"

        actions["Q"] = "Quit the game"

        return actions

    def player_interaction(self):
        self.display_room()
        choice = self.get_player_action()

        # Check for quit action first
        if choice == "Q":
            print("\nThanks for playing!")
            return False

        action_handlers = {
            "F": self.handle_fight,
            "H": self.handle_heal,
            "T": self.handle_take_weapon,
            "A": self.handle_avoid_room
        }

        action_type = choice[0]
        index = int(choice[1:]) - 1 if choice[1:].isdigit() else None

        if action_type in action_handlers:
            result = action_handlers[action_type](index)
            if result is False:
                return False
            elif result is not None:
                self.pause_and_message(result)

            # action_handlers[action_type](index)
        else:
            print("Invalid action. Try again.")

        if len(self.current_room) == 1 and len(self.deck.cards) > 0:
            print("\nYou cleared the room")
            print("Tap Enter to draw a new room...")
            input()

            # Reset turn-specific flags and draw a new room
            self.healed_this_turn = False
            self.avoided_last_room = False
            self.draw_room()

        elif len(self.current_room) == 0 and len(self.deck.cards) == 0:
            print("\nYou cleared the game, congratulations!")
            print("Tap Enter to exit the game...")
            input()
            return False

        return True

    def pause_and_message(self, message):
        self.display_room()
        print(f"\n{message}")
        input("Press Enter to continue...")

    def handle_avoid_room(self, _):
        print("\nAvoiding the room...")
        self.deck.cards.extend(self.current_room)
        self.current_room = []
        self.draw_room()
        self.avoided_last_room = True

    def handle_heal(self, potion_index):
        potions = [card for card in self.current_room if card.suit == "hearts"]
        chosen_potion = potions[potion_index]

        if not self.healed_this_turn:
            self.healed_this_turn = True
            self.health = min(20, self.health + int(chosen_potion.rank))
            self.current_room.remove(chosen_potion)
            self.discard.append(chosen_potion)

            return f"You healed {chosen_potion.rank} HP! Current health: {self.health}"
        else:
            print("You can only heal once per turn! Do you really want to discard this potion?")
            discard_choice = input("\nChoose Y or N: ").strip().upper()
            if discard_choice == "Y":
                self.current_room.remove(chosen_potion)
                self.discard.append(chosen_potion)

                return f"You discarded {chosen_potion}"
            else:
                return None

    def handle_take_weapon(self, weapon_index):
        weapons = [card for card in self.current_room if card.suit == "diamonds"]
        chosen_weapon = weapons[weapon_index]

        self.current_room.remove(chosen_weapon)
        if self.weapon is not None:
            self.discard.append(self.weapon)
            if self.weapon_kills:
                self.discard.extend(self.weapon_kills)
                self.weapon_kills = []
        self.weapon = chosen_weapon

        return f"You took the {chosen_weapon} weapon!"

    def handle_fight(self, monster_index):
        monsters = [card for card in self.current_room if card.suit in ["spades", "clubs"]]
        chosen_monster = monsters[monster_index]

        print("\nHow do you want to fight?")
        print("  [B] Barehanded")
        if self.weapon is not None and (not self.weapon_kills or chosen_monster.value <= self.weapon_kills[-1].value):
            print("  [W] Use weapon")

        fight_choice = None
        while fight_choice not in ["B", "W"]:
            fight_choice = input("\nChoose B or W: ").strip().upper()

        if fight_choice == "B":
            self.health -= chosen_monster.value
            if self.health > 0:
                self.discard.append(chosen_monster)
                self.current_room.remove(chosen_monster)

                return f"You killed {chosen_monster} with your bare hands! Health: {self.health}"
            else:
                print("You lost!")
                return False
        else:
            self.health = self.health if self.weapon.value >= chosen_monster.value else self.health + \
                (self.weapon.value - chosen_monster.value)
            if self.health > 0:
                self.weapon_kills.append(chosen_monster)
                self.current_room.remove(chosen_monster)

                return f"You killed {chosen_monster} using your weapon! Health: {self.health}"
            else:
                print("You lost!")
                return False

    def handle_quit(self, _):
        print("\nThanks for playing!")

    def __repr__(self):
        return f"{len(self.deck.cards)}🂠  - - - - {len(self.discard)}🂠"


game = Scoundrel()

while True:
    # game.player_interaction()
    if not game.player_interaction():
        break
