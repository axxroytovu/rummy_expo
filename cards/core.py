from abc import ABC, abstractmethod

class card(ABC):
    @property
    @abstractmethod
    def name(self):
        return ""

    @property
    @abstractmethod
    def icons(self):
        return ""
    
    def upgrades_into(self):
        return False
    
    @property
    @abstractmethod
    def suit(self):
        pass

    @property
    @abstractmethod
    def value(self):
        pass
    
    @property
    @abstractmethod
    def info(self):
        pass
    
    foil = False
    exp = 0
    
    def on_play(self, game, playstate, player_id):
        pass
    
    def eot(self, game, playstate, player_id):
        pass
    
    def start(self, game, playstate, player_id):
        pass
        
    def game_start(self, game, playstate, player_id):
        pass
    
    def on_discard(self, game, playstate, player_id):
        pass
    
    def on_draw(self, game, playstate, player_id):
        pass
    
    @abstractmethod
    def conditions_met(self, game, playstate, player_id):
        return [], False


class poker_card(card):
    def has_set(self, cards_available):
        count_ = [c for c in cards_available if c.value == self.value]
        return len(count_) >= 3
    
    def conditions_met(self, game, playstate, player_id):
        valid = self.has_set(playstate.orphan_cards + playstate.players[player_id].being_played)
        return [c for c in playstate.orphan_cards if c.value==self.value], valid
    
    def on_play(self, game, playstate, player_id):
        print(f"{playstate.players[player_id].name} played {self.name}")
        vals = {
            "A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "10": 10, "J": 10, "Q": 10, "K": 10
        }
        playstate.players[player_id].score += vals[self.value]

card_database = []

for suit in ["spades", "hearts", "diamonds", "clubs"]:
    for number in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
        name = f"{number} of {suit}"
        icons = f"{suit[0]}{number}"
        vals = {
            "A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "10": 10, "J": 10, "Q": 10, "K": 10
        }
        card_obj = type(icons, (poker_card, ), {
            "name": name,
            "icons": icons,
            "suit": suit,
            "value": number,
            "info": f"Basic poker card. Worth {vals[number]} when played."
        })
        card_database.append(card_obj)
        
        