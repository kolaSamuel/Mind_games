from copy import deepcopy as copy


def play():
    data = open("GameState.txt", 'r')
    game_state = []
    for line in data:
        row = list(map(int, line.split()))
        game_state.append(row)
    data.close()

    data = open("GameState.txt", 'w')

    depth = 2
    size = max(len(game_state), len(game_state[0]))
    inf = 200
    score = [2, 2]
    player = 1

    def _hash(state):
        result = 0
        for i in xrange(size):
            for j in xrange(size):
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

            for i in xrange(size):  # sample(xrange(size), size):
                for j in xrange(size):  # sample(xrange(size), size):
                    if state[i][j] == 2:
                        for x in xrange(-2, 3):  # sample(xrange(-2, 3), 5):
                            if i + x > size - 1 or i + x < 0:
                                continue
                            for y in xrange(-2, 3):  # sample(xrange(-2, 3), 5):
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

            for i in xrange(size):  # sample(xrange(size), size):
                for j in xrange(size):  # sample(xrange(size), size):
                    if state[i][j] == 1:
                        for x in xrange(-2, 3):  # sample(xrange(-2, 3), 5):
                            if i + x > size - 1 or i + x < 0:
                                continue
                            for y in xrange(-2, 3):  # sample(xrange(-2, 3), 5):
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
        return result[1]

    def infect(start, end, _next, state=game_state, scores=score):
        opponent = (_next % 2)+1
        scores[_next-1] += 1
        if any(abs(start[i]-end[i]) == 2 for i in xrange(2)):
            scores[_next-1] -= 1
            state[start[0]][start[1]] = 0

        i, j = end
        state[i][j] = _next
        for x in xrange(-1, 2):
            if i+x > size-1 or i+x < 0:
                continue
            for y in xrange(-1, 2):
                if j + y > size - 1 or j + y < 0:
                    continue
                if state[i+x][j+y] == opponent:

                    scores[_next-1] += 1
                    scores[opponent-1] -= 1
                    state[i+x][j+y] = _next

    a, b, x, y = next_move()
    infect((a, b), (x, y), 1)
    for i in xrange(size):
        print >> data, " ".join(map(str, game_state[i]))
    data.close()
