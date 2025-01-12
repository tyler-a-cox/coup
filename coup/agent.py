import random
from dataclasses import dataclass
from typing import List, Dict, Set, Optional, Tuple

@dataclass
class Character:
    DUKE: str = "Duke"
    ASSASSIN: str = "Assassin"
    CAPTAIN: str = "Captain"
    AMBASSADOR: str = "Ambassador"
    CONTESSA: str = "Contessa"

@dataclass
class Action:
    INCOME: str = "Income"
    FOREIGN_AID: str = "Foreign Aid"
    COUP: str = "Coup"
    TAX: str = "Tax"  # Duke
    ASSASSINATE: str = "Assassinate"  # Assassin
    STEAL: str = "Steal"  # Captain
    EXCHANGE: str = "Exchange"  # Ambassador

class Player:
    def __init__(self, hand, player_id, player_ids=None, coins=2, lie_detector: float=0.2, ):
        """
        Parameters:
        -----------
            hand : list of str
                The cards in the player's hand
            n_coins : int
                The number of coins the player has
        """
        self.hand = hand
        self.revealed = []
        self.coins = coins
        self.player_id = player_id
        self.lie_detector = lie_detector
        self._player_archetype_ = "Default"

        # Prior information on player habits
        self.prior = {}
        if player_ids:
            for player_id in player_ids:
                self.prior[player_id] = {
                    'duke': 0.2,
                    'assassin': 0.2,
                    'captain': 0.2,
                    'ambassador': 0.2,
                    'contessa': 0.2
                }

        # Prior information on center cards
        self.prior_center_cards = {
            'duke': 0.2,
            'assassin': 0.2,
            'captain': 0.2,
            'ambassador': 0.2,
            'contessa': 0.2
        }
        self.active = True

        # Store player move history
        # Thought here is that player habits can be learned by observing their
        # moves. For example, if a player always claims to have a Duke, then
        # is revealed to not have a Duke, then it is likely that the player is
        # lying about having a Duke. This information can be used to make
        # better decisions in the future.
        self.history = {}
        if player_ids:
            for player_id in player_ids:
                self.history[player_id] = []
    
    def get_valid_actions(self):
        """
        """
        valid_actions = [Action.INCOME, Action.FOREIGN_AID]  # Income is always valid
        
        if self.coins >= 10:
            return [Action.COUP]  # Must coup if 7+ coins

        if self.coins >= 7:
            valid_actions.append(Action.COUP)
        
        if self.coins >= 3:
            valid_actions.append(Action.ASSASSINATE)
        
        valid_actions.extend([Action.STEAL, Action.TAX, Action.EXCHANGE])
        return valid_actions

    def challenge_action(self, action):
        """
        Determine if the player will challenge an action
        """
        if action in [Action.INCOME, Action.COUP]:
            return None
        
        challenge_action = random.uniform(0, 1) < self.lie_detector

        if challenge_action:
            # Update player history
            reaction = "challenge" if random.uniform(0, 1) < self.lie_detector else "block"

            if reaction == "block" and action in [Action.TAX, Action.STEAL, Action.EXCHANGE]:
                reaction = "challenge"

            return (reaction,)
            # In the future this will be used to learn player habits
            # self.history[action['player_id']].append(reaction)

        return None
    
    def response_to_challenge(self, action):
        """
        """
        respond_to_challenge = random.uniform(0, 1) < self.lie_detector

        if respond_to_challenge and action[0] == 'block':
            return ('challenge', )
        
        return None
    
    def remove_influence(self, ):
        """
        Remove an influence from the player
        """
        if len(self.hand) > 0:
            self.revealed.append(self.hand.pop())

        self.active = len(self.hand) > 0

    def swap_hand(self, deck):
        card = random.choice(self.hand)
        deck += [card]
        self.hand.remove(card)
        swapped_card = random.choice(deck)
        self.hand += [swapped_card]
        deck.remove(swapped_card)

class AgressivePlayer(Player):
    def __init__(self, hand, player_id, player_ids=None, coins=2, lie_detector: float=0.2):
        super().__init__(hand, player_id, player_ids, coins, lie_detector)
    
    def make_move(self, action, player_id, player_ids, deck):
        """
        """
        if action == Action.COUP:
            return action
        
class TruthfulPlayer(Player):
    def __init__(self, hand, player_id, player_ids=None, coins=2, lie_detector: float=0.2):
        super().__init__(hand, player_id, player_ids, coins, lie_detector)
        self._player_archetype_ = "Truthful"
    
    def get_valid_actions(self):
        """
        """
        valid_actions = [Action.INCOME, Action.FOREIGN_AID]  # Income is always valid
        
        if self.coins >= 10:
            return [Action.COUP]  # Must coup if 7+ coins
        if self.coins >= 7:
            valid_actions.append(Action.COUP)
        if self.coins >= 3 and Character.ASSASSIN in self.hand:
            valid_actions.append(Action.ASSASSINATE)
        if Character.DUKE in self.hand:
            valid_actions.append(Action.TAX)
        if Character.CAPTAIN in self.hand:
            valid_actions.append(Action.STEAL)
        if Character.AMBASSADOR in self.hand:
            valid_actions.append(Action.EXCHANGE)
        
        return valid_actions
        
class RandomPlayer(Player):
    def __init__(self, hand, player_id, player_ids=None, coins=2, lie_detector: float=0.2):
        super().__init__(hand, player_id, player_ids, coins, lie_detector)
    
    def make_move(self, action, player_id, player_ids, deck):
        """
        """
        if action == Action.COUP:
            return action