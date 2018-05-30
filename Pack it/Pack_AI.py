import json
from collections import Counter
from random import sample, shuffle

import sys

depth_count = Counter()
total = 0
ob_lim = 10**4

level = 'Pack it 2'
with open("game_state.json") as file:
    data = json.load(file)
    pieces = data['Pieces']

board_length = 8
board_breadth = 8
board = [[0]*board_breadth for _ in range(board_length)]
# board = [
#     [0, 1, 1, 1, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 0, 0],
#     [1, 1, 1, 1, 1, 1, 0, 0],
#     [0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1],
#     [0, 1, 1, 1, 0, 0, 1, 0],
# ]
game = data[level]
all_pieces = Counter()
piece_children = dict()
seen = set()
goal = 0
depth = 0
for (x, y) in game:
    all_pieces[x] = y
    goal += y


def observe():  # move, zero, extra):
    global total
    total += 1
    depth_count[depth] += 1
    if total % ob_lim == 0:
        print(depth_count)
    # if depth == 5:
    #     print(move, zero, extra)
    #     display()


def display():
    for i in range(board_length):
        for j in range(board_breadth):
            if board[i][j]:
                if board[i][j] == 1:
                    board[i][j] = ord('.')
                board[i][j] = chr(board[i][j])
            else:
                board[i][j] = '-'
    print(*board, sep='\n')
    sys.exit()


def heuristic(move):
    piece, pos = move
    insert(piece, -1, pos)
    x, y = pos
    result = 0
    for i in range(x+1):
        for j in range(board_breadth):
            if board[i][j] == 0:
                result += 1
            if i == x and j == y:
                insert(piece, -1, pos, False)
                return result


def insert(piece, d, pos, place=True):
    symbol = d + ord('A')
    symbol *= int(place)
    x, y = pos
    length = len(piece)
    breadth = len(piece[0])
    for i in range(length):
        for j in range(breadth):
            if piece[i][j]:
                board[i+x][j+y] = symbol


def get_child(piece):
    result = []
    length = len(piece)
    breadth = len(piece[0])
    shift = True
    zero = 0

    for x in range(board_length - length + 1):
        for y in range(board_breadth - breadth + 1):
            checker = 0
            extra = 0

            for i in range(length):
                for j in range(breadth):
                    checker = piece[i][j] * board[x + i][y + j]
                    if piece[i][j] + board[x + i][y + j] == 0 and i != length-1 and j != breadth-1:
                        extra += 1

                    if checker: break
                if checker: break
            else:
                move = (piece, (x, y))
                if zero+extra > 7:
                    # observe(move, zero, extra)
                    return result
                result.append(move)
                if shift:
                    shift = False
                    continue
                return result

            if board[x][y] == 0:
                zero += 1
                if zero > 7:
                    # observe("None", zero, 0)
                    return result
    return result


def get_all_children(piece_array):
    result = []

    for piece in piece_array:
        moves = get_child(piece)
        if len(moves):
            result.extend(moves)

    return result


def trim(matrix):
    # remember to fix this if it works
    return matrix[:]
    new = []
    # row trim
    for row in matrix:
        if sum(row):
            new.append(row[:])

    # column trim
    breadth = len(new[0])
    for i in range(breadth-1, -1, -1):
        if not(sum(new[j][i] for j in range(len(new)))):
            for j in range(len(new)):
                del(new[j][i])
    return new


def reflections(masks, piece):
    result = []

    # vertical reflection
    for _ in range(2):
        for row in piece:
            row.reverse()
        mask = hashed(piece)

        if not(mask in masks):
            masks.append(mask)
            result.append(trim(piece))

    # horizontal reflection
    for _ in range(2):
        piece.reverse()
        mask = hashed(piece)

        if not(mask in masks):
            masks.append(mask)
            result.append(trim(piece))

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


def hashed(matrix, s_hash=False):
    result = 0
    if s_hash:
        result = list(map(hashed, rotations(matrix)))
    else:
        for row in matrix:
            for x in row:
                result <<= 1
                if x:
                    result |= 1
    return result


for x in all_pieces:
    piece_index = str(x)
    piece_children[x] = rotations(pieces[piece_index])


def dfs_solve():
    global depth

    for x in sample(all_pieces.keys(), len(all_pieces)):
        if all_pieces[x]:
            all_pieces[x] -= 1
            all_children = get_all_children(piece_children[x])
            # all_children.sort(key=heuristic)
            shuffle(all_children)
            for child in all_children:
                piece, pos = child
                insert(piece, depth, pos)
                masks = hashed(board, s_hash=True)
                if any(mask in seen for mask in masks):
                    insert(piece, -1, pos, False)
                    depth_count['repeated'] += 1
                    continue
                seen.update(masks)
                depth += 1
                observe()
                if depth == goal or dfs_solve():
                    # for child in all_children:
                    #     print(*child[0], child[1], '', sep='\n')
                    # display()
                    return True
                depth -= 1
                insert(piece, -1, pos, False)
        all_pieces[x] += 1
    return False


if dfs_solve():
    display()
else:
    print('Guy False')
print('Done')
