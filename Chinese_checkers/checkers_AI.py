import json
game_piece = 1
level = "Checkers 1"
with open("game_state.json") as file:
    data = json.load(file)

game_state = data[level]["game_state"]
goal = data[level]["goal"]
legal_moves = data["legal_moves"]
swaps = data["swaps"]
transitions = data["transitions"]
length = len(game_state)
breadth = len(game_state[0])
visited = set()
solution = []


def play(move, f=0):
    x, y, direction = move
    _x = x + swaps[direction][0]
    _y = y + swaps[direction][1]
    # swaps
    game_state[x][y], game_state[_x][_y] = \
        game_state[_x][_y], game_state[x][y]
    # transition effect
    _x = x + transitions[direction][0]
    _y = y + transitions[direction][1]
    game_state[_x][_y] = f


def effect(x, y):
    result = 0
    for (i, j) in transitions.values():
        if not game_state[x+i][y+j] % 2:
            result += 1
    return result


def heuristic(move):
    h = 0
    x, y, direction = move
    h += effect(x, y)
    # transition
    x += transitions[direction][0]
    y += transitions[direction][1]
    h += effect(x, y)
    # swap
    x += transitions[direction][0]
    y += transitions[direction][1]
    h -= effect(x, y)
    return h


def get_successors():
    successors = []
    for i in range(length):
        for j in range(breadth):
            if game_state[i][j] == game_piece:
                for (x, y, direction) in legal_moves:
                    if not(0 <= i+x < length and 0 <= j+y < breadth):
                        continue
                    if game_state[i+x][j+y] == 0:
                        _x = i + transitions[direction][0]
                        _y = j + transitions[direction][1]
                        if game_state[_x][_y] != game_piece:
                            continue
                        successors.append((i, j, direction))
    if data["heuristic"]:
        successors.sort(key=heuristic, reverse=True)
    return successors


def hashed():
    result = 0
    for layer in game_state:
        for piece in layer:
            result *= 10
            result += piece
    return result


def dfs_solve():
    mask = hashed()
    if mask in visited:
        return False
    visited.add(mask)
    moves = get_successors()
    if len(moves) == 0:
        return False
    for move in moves:
        play(move)
        solution.append(move)
        if len(solution) == goal or dfs_solve():
            return True
        play(move, game_piece)
        solution.pop()


def display():
    for move in game_state:
        play(move)
        with open("game_play.txt", "w") as game_play:
            print('\n', *game_state, sep='\n', file=game_play)
            print("\n\tMove :", move, file=game_play)
        input('Next...')


if __name__ == "__main__":
    dfs_solve()
    if len(solution):
        print(*solution, sep="\n")
        print(len(solution))
    else:
        print("No solution Found: ",
              "\n\tIt's not you, it's me.",
              "\n\tBut... check game state to be sure")
