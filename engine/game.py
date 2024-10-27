from abc import ABC, abstractmethod
import random

class player():
    def __init__(self, deck, controller, name=""):
        self.name = name
        self.deck = deck
        random.shuffle(self.deck)
        self.hand = []
        self.being_played = []
        self.in_play = []
        self.discard = []
        self.score = 0
        self.handsize = 10
        self.controller = controller
    
    def draw_start(self, game_, playstate_, player_id):
        for _ in range(self.handsize):
            self.hand.append(self.deck.pop())
        for c in self.hand:
            c.on_draw(game_, playstate_, player_id)
    
    def draw(self, game_, playstate_, player_id):
        discard_card = self.controller.draw_ai(player_id, playstate_)
        discard_card.on_discard(game_, playstate_, player_id)
        print(f"{playstate_.players[player_id].name} discarded {discard_card.name}")
        self.discard.append(discard_card)
        self.hand.remove(discard_card)
        while len(self.hand) < self.handsize:
            self.hand.append(self.deck.pop())
    
    def play(self, playstate_, player_id):
        playcards = self.controller.play_ai(player_id, playstate_)
        for c in playcards:
            self.being_played.append(c)
            self.hand.remove(c)
        

class playstate():
    def __init__(self, decks, controllers, names):
        self.players = [player(*d) for d in zip(decks, controllers, names)]
        self.players[0].is_PC = True
        self.orphan_cards = []
        self.revealed = [[] for i in range(len(decks))]
    
    def calculate(self, game_):
        for i, p in sorted(enumerate(self.players), key=lambda v: v[1].score):
            for card in list(p.being_played):
                if card.conditions_met(game_, self, i):
                    card.on_play(game_, self, i)
                else:
                    print(f"Player {i} played orphan card {card.icons}")
                    p.being_played.remove(card)
                    self.orphan_cards.append(card)
            p.in_play.extend(p.being_played)
            p.being_played = []
    
    def trigger_eot(self, game_):
        for i, p in sorted(enumerate(self.players), key=lambda v: v[1].score):
            for card in list(p.in_play):
                card.eot(game_, self, i)


class game():
    def __init__(self, decks, controllers, names, target):
        self.playercount = len(decks)
        self.playstate = playstate(decks, controllers, names)
        self.target = target
    
    def play(self):
        self.game_start()
        active = True
        while active:
            self.draw()
            self.play_cards()
            self.on_play()
            active = self.eot()
    
    def game_start(self):
        for p in range(self.playercount):
            for c in self.playstate.players[p].deck:
                c.game_start(self, self.playstate, p)
            self.playstate.players[p].draw_start(self, self.playstate, p)
    
    def draw(self):
        for p in range(self.playercount):
            self.playstate.players[p].draw(self, self.playstate, p)
    
    def play_cards(self):
        for p in range(self.playercount):
            self.playstate.players[p].play(self.playstate, p)
    
    def on_play(self):
        self.playstate.calculate(self)
    
    def eot(self):
        self.playstate.trigger_eot(self)
        for p in self.playstate.players:
            print(f"{p.name} score: {p.score}")
        if any([p.score > self.target for p in self.playstate.players]):
            victor = sorted(self.playstate.players, key=lambda k: k.score, reverse=True)[0]
            print(f"{victor.name} Wins!")
            return False
        return True
