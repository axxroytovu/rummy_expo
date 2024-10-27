import random
from abc import ABC, abstractmethod
import itertools as itr

class controller(ABC):
    @property
    @abstractmethod
    def is_player(self):
        return False
    
    @abstractmethod
    def draw_ai(self, player_id, playstate):
        pass
    
    @abstractmethod
    def play_ai(self, player_id, playstate):
        pass
    
class player(controller):
    is_player = True
    
    def draw_ai(self, player_id, playstate):
        playstate.display()
        discard_id = int(input("Choose a card to discard: "))
        return playstate.players[player_id].hand[discard_id]

    def play_ai(self, player_id, playstate):
        playstate.display()
        play_ids = input("Choose any number of cards to play separated by commas: ")
        try:
            play_cards = [playstate.players[player_id].hand[int(i)] for i in play_ids.split(",")]
        except ValueError:
            play_cards = []
        return play_cards

class sets_only(controller):
    is_player = False
    
    def draw_ai(self, player_id, playstate):
        vals = {}
        hand = playstate.players[player_id].hand
        for c in hand:
            if c.value not in vals:
                vals[c.value] = 0
            vals[c.value] += 1
        val = sorted([(c, v) for v, c in vals.items()])[0][1]
        return next(c for c in hand if c.value == val)
    
    def play_ai(self, player_id, playstate):
        vals = {}
        play_cards = []
        hand = playstate.players[player_id].hand
        for c in itr.chain(hand, playstate.orphan_cards):
            if c.value not in vals:
                vals[c.value] = 0
            vals[c.value] += 1
        for v, n in vals.items():
            if n >= 3:
                play_cards.extend([c for c in hand if c.value == v])
        return play_cards
                