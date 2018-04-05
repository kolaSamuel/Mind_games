from copy import deepcopy as copy
from random import sample
from timeit import timeit

depth = 2
size = 7
inf = 200
game_state = [[0]*size for _ in range(size)]
game_state[0][0] = game_state[size-1][size-1] = 2
game_state[0][size-1] = game_state[size-1][0] = 1
score = [2, 2]
player = 1


def _hash(state):
    result = 0
    for i in range(size):
        for j in range(size):
            result *= 10
            result += state[i][j]
    return result


def next_move():
    my_visit = set()
    opponent_visit = set()

    def opponent(state, look_ahead, scores, alpha=-inf):
        _min = inf

        value = _hash(state)
        if value in opponent_visit:
            return -inf
        opponent_visit.add(value)

        for i in range(size):  # sample(range(size), size):
            for j in range(size):  # sample(range(size), size):
                if state[i][j] == 2:
                    for x in range(-2, 3):  # sample(range(-2, 3), 5):
                        if i + x > size - 1 or i + x < 0:
                            continue
                        for y in range(-2, 3):  # sample(range(-2, 3), 5):
                            if j + y > size - 1 or j + y < 0:
                                continue
                            if x + y == 0: continue
                            if not state[i+x][j+y]:
                                new_state = copy(state)
                                new_score = copy(scores)
                                infect((i, j), (i+x, j+y), 2, new_state, new_score)

                                _min = min(_min, me(new_state, look_ahead, new_score, _min)[0])
                                if _min < alpha:
                                    return _min

        return _min

    def me(state=game_state, look_ahead=depth, scores=score, beta=inf):
        look_ahead -= 1
        _max = (-inf, (0, 0, 0, 0))

        value = _hash(state)
        if value in my_visit:
            return [inf, 0]
        my_visit.add(value)

        for i in range(size):  # sample(range(size), size):
            for j in range(size):  # sample(range(size), size):
                if state[i][j] == 1:
                    for x in range(-2, 3):  # sample(range(-2, 3), 5):
                        if i + x > size - 1 or i + x < 0:
                            continue
                        for y in range(-2, 3):  # sample(range(-2, 3), 5):
                            if j + y > size - 1 or j + y < 0:
                                continue
                            if x + y == 0: continue
                            if not state[i+x][j+y]:
                                new_state = copy(state)
                                new_score = copy(scores)
                                infect((i, j), (i+x, j+y), 1, new_state, new_score)

                                if look_ahead:
                                    effect = opponent(new_state, look_ahead, new_score, _max[0])
                                else:
                                    effect = new_score[0] - new_score[1]

                                _max = max(_max, (effect, (i, j, i + x, j + y)))
                                if _max[0] > beta:
                                    return _max
        return _max
    result = me()
    print('suggested move', result)
    return result[1]


def infect(start, end, _next, state=game_state, scores=score):
    opponent = (_next % 2)+1
    scores[_next-1] += 1
    if any(abs(start[i]-end[i]) == 2 for i in range(2)):
        scores[_next-1] -= 1
        state[start[0]][start[1]] = 0

    i, j = end
    state[i][j] = _next
    for x in range(-1, 2):
        if i+x > size-1 or i+x < 0:
            continue
        for y in range(-1, 2):
            if j + y > size - 1 or j + y < 0:
                continue
            if state[i+x][j+y] == opponent:

                scores[_next-1] += 1
                scores[opponent-1] -= 1
                state[i+x][j+y] = _next


def end_state(player, state=game_state):
    """

    :param player:
    :param state:
    :return: True if the player can no longer make a
            move
    """
    for i in range(size):
        for j in range(size):
            if state[i][j] == player:
                for x in range(-2, 3):
                    if i + x > size - 1 or i + x < 0:
                        continue
                    for y in range(-2, 3):
                        if j + y > size - 1 or j + y < 0:
                            continue
                        if x+y == 0: continue
                        elif state[i+x][j+y] == 0:
                            return False
    return True


def display_state():
    """

    :return: prints out current game state
    """
    for x in game_state:
        print('\t', x)
    print('\n')
    print('You :', score[1])
    print('Me  :', score[0])


while not end_state(player):
    display_state()
    if player == 2:
        a, b, x, y = list(map(int, input('Move : ').split()))
    else:
        # print(timeit('next_move()', setup='from __main__ import next_move', number=1))
        # input('Chill..')
        a, b, x, y = next_move()
    try:
        assert(game_state[a][b] == player)
        assert(game_state[x][y] == 0)
        assert(all(-1 < val < size for val in [a, b, x, y]))
        assert(all(abs(val[0]-val[1]) < 3 for val in [(a, x), (b, y)]))
    except AssertionError:
        print("Impossible Move...")
        continue

    infect((a, b), (x, y), player)

    #
    # cool maths to cause values to alternate between 1 and 2
    player = (player % 2)+1

display_state()
print('Game Over')
