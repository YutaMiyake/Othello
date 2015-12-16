# Othello
A simple AI plays othello using minimax algorithm with alpha-beta pruning

## Description
CPU has three levels. Level 1 plays randomly. Level 2 and 3 play under minimax strategy. The minimax search is a combination of a cut-off search (with depth = 4) with alpha-beta pruning.The difference between level 2 and 3 comes from what heuristic evaluation function is used. For level 2, a state is evaluated by simply counting the number of pieces (+1 or -1). For level 3, a heuristic value is calculated according to predefined matrix (e.g., corners are more valuable) + time-variant penalty (as the current state becomes closer to the last stage, each player will get more penalty/bonus if the number of his color is less/more than the other at the current state).

## Installation
* python 2.7
* numpy

## Usage
```
> python othello.py
```
## Screenshots
![Alt testcase](./images/screenshot1.png?raw=true "testcase")

## Minimax Tree
![Alt minimaxtree](./graph_out/minimax_tree.png?raw=true "minimaxtree")

## Licence
* MIT License

## Author
* Yuta Miyake
