"""
    Re-run if it doesn't solve in 5 minutes
    Might need to run program more than once typically < 5.
"""

import json
from collections import defaultdict
from itertools import combinations as combine
from random import shuffle
import sys

level = "Domino 4"
with open("game_state.json") as file:
    data = json.load(file)


# initializations
length = data[level]["length"]
breadth = data[level]["breadth"]
goal = data[level]["goal"]
horizontal = [0]*length
vertical = [0]*length
total_pieces = length*breadth
game_state = []
game_state_set = set()
count = 0
pieces = data["General"]["pieces"]
# pieces.sort(reverse=True)

# MOST IMPORTANT LINE OF CODE, DO NOT CHANGE
shuffle(pieces)
# ******************************************

checker = breadth/2
combinations = dict()
new_pieces = set()


def get_game_state():
    return game_state


def to_tuple(x):
    y = (x[0], x[1])
    if x[0] > x[1]:
        y = (x[1], x[0])
    return y


for x in pieces:
    new_pieces.add(to_tuple(x))

for comb in range(1, breadth+1):
    combinations[comb] = defaultdict(list)
    for combs in combine(new_pieces, comb):
        x = sum([sum(x) for x in combs])
        if x > goal:
            continue
        combinations[comb][x].append(set(combs))

diagonal = [0]*2


def forward_checking(pos):
    """
        Uses forward checking to speed up CSP
    :param pos: current filled position
    :return: True if forward checking passed, False otherwise
    """
    horizontal_check = pos % length
    vertical_check = breadth - (pos//length)

    left = vertical_check - 1
    right = vertical_check

    for v in range(length):
        target = goal - vertical[v]
        index = left
        if v > horizontal_check:
            index = right
        if index == 0 or any(x.isdisjoint(game_state_set) for x in combinations[index][target]):
            continue
        return False
    return True


def valid(x, f=1):
    """
    Checks if the piece placed violates any constrain in the CSP
    :param x: current piece to be placed
    :param f: 1 if chip is being placed -1 if it is being removed
    :return: True of False values
    """

    # Maths to determine positions
    size = len(game_state)
    h = (size//length)*2
    v = size % length

    horizontal[h] += x[0]*f
    horizontal[h+1] += x[1]*f
    vertical[v] += (x[0]+x[1])*f
    for d in range(2):
        if h+d == v:
            diagonal[0] += x[d]*f
        if h+d+v == length-1:
            diagonal[1] += x[d]*f

    if f == -1:
        return

    if any(x > goal for x in [horizontal[h], horizontal[h+1],
                              vertical[v], *diagonal]):
        return False
    # length-1, last element on row
    if size % length == length-1:
        if any(horizontal[x] < goal for x in [h, h+1]):
            return False
    if size == total_pieces-length+1 or size == total_pieces-1:
        if diagonal[size//(total_pieces-1)] < goal:
            return False
    if size > length*(breadth-1)-1:
        if any(vertical[x] < goal for x in range(v+1)):
            return False
    if 0 < size < total_pieces-1 and not(size % checker):
        return forward_checking(size+1)

    return True


def back_track():
    """
    DFS which solves CSP
    :return: True if path possible, False if not
    """
    for x in pieces:
        y = x[::-1]
        z = to_tuple(x)
        if x in game_state or y in game_state:
            continue
        if valid(x):
            game_state.append(x)
            game_state_set.add(z)
            if len(game_state) == total_pieces or back_track():
                return True
            game_state.pop()
            game_state_set.remove(z)
        valid(x, -1)
    return False


if __name__ == "__main__":
    back_track()
    # print(diagonal_positions, sep="\n")
    print('\n', game_state)
    print('h: ', horizontal)
    print('v: ', vertical)
    print('d: ', diagonal)
