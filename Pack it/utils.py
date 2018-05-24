import json
from collections import Counter
from copy import deepcopy as copy
import sys

level = 'Pack it 2'
with open("game_state.json") as file:
    data = json.load(file)
    pieces = data['Pieces']

board = [['_']*8 for _ in range(8)]
game = data[level]
all_pieces = Counter()
piece_children = dict()
total_pieces = 0
for (x, y) in game:
    all_pieces[x] = y
    total_pieces += y


def reflections(masks, piece):
    result = []

    # vertical reflection
    for _ in range(2):
        for row in piece:
            row.reverse()
        mask = hashed(piece)

        if not(mask in masks):
            masks.append(mask)
            result.append(copy(piece))

    # horizontal reflection
    for _ in range(2):
        piece.reverse()
        mask = hashed(piece)

        if not(mask in masks):
            masks.append(mask)
            result.append(copy(piece))

    return result


def rotations(piece):
    length = len(piece)
    result = []
    masks = []

    # number of rotations
    for _ in range(5):
        new_piece = [[] for _ in range(length)]
        for x in range(length):
            for y in range(length-1, -1, -1):
                new_piece[x].append(piece[y][x])
        piece = new_piece
        result.extend(reflections(masks, piece))

    return result


def hashed(matrix):
    result = 0
    for row in matrix:
        for x in row:
            result <<= 1
            result |= x
    return result


for x in all_pieces:
    piece_index = str(x)
    piece_children[x] = rotations(pieces[piece_index])

print('done')
