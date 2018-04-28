import json
# from random import shuffle
test = [(3, 7, 'down'), (3, 5, 'right'), (1, 5, 'down'), (1, 3, 'right'), (2, 3, 'right'),
        (2, 6, 'left'), (3, 4, 'right'), (3, 2, 'right'), (3, 4, 'up'), (1, 5, 'left'),
        (3, 7, 'left'), (5, 2, 'up'), (3, 1, 'right'), (4, 3, 'up'), (1, 3, 'down'),
        (4, 5, 'left'), (5, 4, 'left'), (5, 1, 'right'), (5, 6, 'left'), (7, 5, 'up'),
        (5, 4, 'right'), (5, 7, 'left'), (6, 3, 'right'), (4, 3, 'down'), (6, 6, 'left'),
        (7, 3, 'up'), (7, 4, 'up'), (5, 4, 'right'), (5, 6, 'up'), (3, 6, 'left'),
        (3, 4, 'left'), (2, 2, 'down'), (4, 1, 'right'), (4, 3, 'down'), (6, 2, 'right')]
game_piece = 1
level = "Checkers 2"
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
    # shuffle(successors)
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
            print(*game_state, sep='\n', file=game_play)
            print("\n\tMove :", move, file=game_play)
        input('Next...')


dfs_solve()
if __name__ == "__main__":
    if len(solution):
        print(*solution, sep="\n")
        print(len(solution))
    else:
        print("No solution Found: ",
              "\n\tIt's not you, it's me.",
              "\n\tBut... check game state to be sure")
