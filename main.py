import sys
from os import system
from abc import ABC, abstractmethod
from engine import game, controllers
from cards.core import card_database

class menu_option(ABC):
    @abstractmethod
    def call(self):
        pass
    
    @property
    @abstractmethod
    def name(self):
        pass

def build_deck():
    deck = []
    for card in card_database:
        deck.append(card())
    return deck

class game_container():
    def __init__(self):
        self.main_menu = dict(enumerate([self.load_save_mo(), self.play_game_mo(), self.quit_mo()]))

    def display_menu(self, menu_options):
        for k, function in menu_options.items():
            print(k, function.name)
    
    class load_save_mo(menu_option):
        def call(self):
            pass
        name = "load save file"
    
    class play_game_mo(menu_option):
        def call(self):
            active_game = game.game([build_deck(), build_deck()], 
                                    [controllers.player(), controllers.sets_only()], 
                                    ["You", "Jim"], 50)
            active_game.play()
        name = "play game"
    
    class quit_mo(menu_option):
        def call(self):
            sys.exit()
        name = "quit"

if __name__ == "__main__":
    gc = game_container()
    while True:
        print()
        gc.display_menu(gc.main_menu)
        selection = int(input("Menu option: "))
        gc.main_menu[selection].call()
