import json
import sys

level = "Domino 2"
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
pieces = []


def convert_to_d(array):
    result = []
    for position in array:
        x = (position // length) * 2
        y = position % length
        result.extend([(x, y), (x, y+1)])
    return set(result)


diagonal_positions = {
    0: convert_to_d([x for x in range(0, total_pieces, length+2)]),
    1: convert_to_d([x for x in range(length*(breadth-1), 1, -(length-2))]),
}
diagonals = [0]*2

for i in range(7):
    for j in range(7):
        if i+j > goal:
            continue
        pieces.append((i, j))


def forward_checking():
    return True


def valid(x, f=1):
    # Maths to determine positions
    size = len(game_state)
    h = (size//length)*2
    v = size % length

    horizontal[h] += x[0]*f
    horizontal[h+1] += x[1]*f
    vertical[v] += (x[0]+x[1])*f
    for d in range(2):
        if (h, v) in diagonal_positions[d]:
            d_index = (v + d) % 2
            diagonals[d] += x[d_index]*f

    if any(x > goal for x in [horizontal[h], horizontal[h+1],
                              vertical[v], diagonals[0], diagonals[1]]):
        return False
    # length-1, last element on row
    if size % length == length-1:
        if any(horizontal[x] < goal for x in [h, h+1]):
            return False
    if size == total_pieces-length+1 or size == total_pieces-1:
        if diagonals[size//(total_pieces-1)] < goal:
            return False
    if size > length*(breadth-1)-1:
        if any(vertical[x] < goal for x in range(v+1)):
            return False
    if 0 < size < total_pieces-1 and not(size%length):
        return forward_checking()

    return True


def back_track():
    for x in pieces:
        y = x[::-1]
        if x in game_state:
            continue
        if y in game_state:
            continue
        if valid(x):
            game_state.append(x)
            # if len(game_state) == 12:
            #     print(game_state)
            #     print(diagonals)
            #     sys.exit()
            if len(game_state) == total_pieces or back_track():
                return True
            game_state.pop()
        valid(x, -1)
    return False


back_track()
# print(diagonal_positions, sep="\n")
print('\n', game_state)
print('h: ', horizontal)
print('v: ', vertical)
print('d: ', diagonals)
