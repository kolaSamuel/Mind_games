import sys
length = 4
breadth = 2
goal = 6
game_state = []
pieces = []
horizontal = [0]*4
vertical = [0]*4
diagonals = [0]*2

for i in range(7):
    for j in range(7):
        if i+j > 6: continue
        pieces.append((i, j))


def valid(x, f=1):
    # Maths to determine positions
    size = len(game_state)
    h = (size//4)*2
    v = size % 4
    d = int((h//2) == (v < 2))
    d_index = (v+d) % 2

    horizontal[h] += x[0]*f
    horizontal[h+1] += x[1]*f
    vertical[v] += (x[0]+x[1])*f
    diagonals[d] += x[d_index]*f

    if any(x > 6 for x in [horizontal[h], horizontal[h+1],
                           vertical[v], diagonals[d]]):
        return False
    if size == 3:
        if any(horizontal[x] < 6 for x in range(2)):
            return False
    elif size == 5 or size == 7:
        if diagonals[size//7] < 6:
            return False
    if size > 3:
        if any(vertical[x] < 6 for x in range(v+1)):
            return False

    return True


def back_track():
    for x in pieces:
        y = x[::-1]
        if x in game_state: continue
        if y in game_state: continue
        if valid(x):
            game_state.append(x)
            if len(game_state) == 8 or back_track():
                return True
            game_state.pop()
        valid(x, -1)
    return False


back_track()
print('\n', game_state)
print('h: ', horizontal)
print('v: ', vertical)
print('d: ', diagonals)
