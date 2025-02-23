import os
from deck import Deck


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
        self.weapon = None
        self.weapon_kills = []

        self.current_room = []
        self.avoided_last_room = False
        self.draw_room()

    def avoid_room(self):
        if self.avoided_last_room:
            print("You cannot avoid two rooms in a row!")
            return

        print("Avoiding the room...")
        print("\n===================================================")

        self.deck.cards.extend(self.current_room)
        self.current_room = []
        self.draw_room()
        self.avoided_last_room = True

    def take_weapon(self, weapon_index):
        weapons = [
            card for card in self.current_room if card.suit in ["diamonds"]]

        chosen_weapon = weapons[weapon_index]

        print(f"You took the {chosen_weapon} weapon!")
        self.current_room.remove(chosen_weapon)
        if self.weapon is None:
            self.weapon = chosen_weapon
            print(
                f"You took {chosen_weapon}!")
        else:
            print(
                f"You took {chosen_weapon}! Discarding {self.weapon}")
            self.discard.append(self.weapon)
            if self.weapon_kills != []:
                self.discard.append(self.weapon_kills)
            self.weapon = chosen_weapon

    def fight(self, monster_index):
        monsters = [
            card for card in self.current_room if card.suit in ["spades", "clubs"]]
        
        chosen_monster = monsters[monster_index]

        if self.weapon:
            print("\nHow do you want to fight?")
            print("  [B] Barehanded")
            if chosen_monster.rank <= max(self.weapon_kills, default=0):
                print(f"  [W] Use weapon (Kills: {self.weapon_kills}, Max Rank: {max(self.weapon_kills, default=0)})")

            fight_choice = None
            while fight_choice not in ["B", "W"]:
                fight_choice = input("\nChoose B or W: ").strip().upper()
            
            

    def heal(self, potion_index):
        potions = [
            card for card in self.current_room if card.suit in ["hearts"]]

        chosen_potion = potions[potion_index]

        self.health = min(20, self.health + int(chosen_potion.rank))
        self.current_room.remove(chosen_potion)
        self.discard.append(chosen_potion)

        print(
            f"You healed {chosen_potion.rank} HP! Current health: {self.health}")

    def draw_room(self):
        num_cards = 4 - len(self.current_room)
        self.current_room = [self.deck.draw() for _ in range(num_cards)]

    def display_room(self):
        clear_screen()
        tab_count = 2 if len(self.current_room) <= 2 else 1
        tabs = "\t" * tab_count

        print(f"{len(self.deck.cards)}🂠 \t" + " ".join(map(str,
              self.current_room)) + f"{tabs}{len(self.discard)}🂠")
        print(f"Health: {self.health}")
        print(f"Weapon: {self.weapon}" + " ".join(map(str, self.weapon_kills)))

        actions = self.get_available_actions()

        print("\nAvailable Actions:")
        for key, desc in actions.items():
            print(f"  [{key}] {desc}")

    def get_available_actions(self):
        actions = {}

        monsters = [card for card in self.current_room if card.suit in [
            "spades", "clubs"]]
        potions = [card for card in self.current_room if card.suit in ["hearts"]]
        weapons = [
            card for card in self.current_room if card.suit in ["diamonds"]]

        # Assign numbered actions for multiple monsters
        for i, monster in enumerate(monsters):
            actions[f"F{i+1}"] = f"Fight {monster}"

        # Assign numbered actions for multiple potions
        for i, potion in enumerate(potions):
            actions[f"H{i+1}"] = f"Use {potion}"

        # Assign numbered actions for multiple weapons
        for i, weapon in enumerate(weapons):
            actions[f"T{i+1}"] = f"Take {weapon}"

        if not self.avoided_last_room:
            actions["A"] = "Avoid this room"

        actions["Q"] = "Quit the game"

        return actions

    def player_interaction(self):
        self.display_room()
        actions = self.get_available_actions()

        while True:
            choice = input("\nChoose an action: ").strip().upper()

            if not choice:
                clear_screen()
                self.display_room()
                continue

            if choice in actions:
                if choice.startswith("F"):
                    index = int(choice[1:]) - 1
                    self.fight(index)
                elif choice.startswith("H"):
                    index = int(choice[1:]) - 1
                    self.heal(index)
                elif choice.startswith("T"):
                    index = int(choice[1:]) - 1
                    self.take_weapon(index)
                elif choice == "A":
                    self.avoid_room()
                elif choice == "Q":
                    print("Thanks for playing!")
                    return False  # Exit game loop
                break
            else:
                print("Invalid choice. Try again.")

        return True  # Continue game loop

    def __repr__(self):
        return f"{len(self.deck.cards)}🂠  - - - - {len(self.discard)}🂠"


game = Scoundrel()

while True:
    # game.player_interaction()
    if not game.player_interaction():
        break
