# Coup

## Model

Two part model for a game-playing AI for Coup. 

### Prediction Model

The first in the two part model is a Bayesian model which attempts to predict which players have which cards based on the actions they take throughout the game (and possibly between games).

Provides some insight into the cards that a player may have.

### Action Model

The second is a model which determines the best actions to take given a history of decisions made by alternate players