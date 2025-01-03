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
    def __init__(self, hand, player_id, player_ids=None, coins=2):
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
    
    def challenge_action(self, action):
        """
        Determine if the player will challenge an action
        """
        if action in [Action.INCOME, Action.COUP]:
            return None
        
        challenge_action = random.uniform(0, 1) < 0.2

        if challenge_action:
            # Update player history
            reaction = "challenge" if random.uniform(0, 1) < 0.2 else "block"

            return (reaction,)
            # In the future this will be used to learn player habits
            # self.history[action['player_id']].append(reaction)

        return None
    
    def remove_influence(self, ):
        """
        Remove an influence from the player
        """
        self.revealed.append(self.hand.pop())