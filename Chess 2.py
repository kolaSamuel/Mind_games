from collections import Counter
import sys

sys.setrecursionlimit(50000)

length, breadth = 4, 5
black, white = Counter(), Counter()
for i in range(length):
    black[(i, 0)] = 1
    white[(i, breadth-1)] = 1

solution = []
seen = set()
pending = set()


def hashed(black_piece=black, white_piece=white):
    value = 0
    for i in range(length):
        for j in range(breadth):
            value *= 10
            if black_piece[(i, j)]:
                value += 1
            elif white_piece[(i, j)]:
                value += 2
    return value


goal = int(str(hashed())[::-1])
print(goal)


def display(black_piece=black, white_piece=white):
    board = [['-']*breadth for _ in range(length)]
    for x in black_piece:
        if black_piece[x]:
            board[x[0]][x[1]] = 'B'
    for x in white_piece:
        if white_piece[x]:
            board[x[0]][x[1]] = 'W'

    print(*board, sep='\n')
    print()


def get_valid_moves(black_piece=black, white_piece=white):
    moves = []
    for i in range(length):
        for j in range(breadth):
            pos = (i, j)
            if black_piece[pos] or white_piece[pos]:
                continue
            for (x, y) in black_piece:
                if black_piece[(x, y)] == 0:
                    continue
                if abs(i-x) != abs(j-y):
                    continue
                elif any(abs(i-x1) == abs(j-y1) and white_piece[(x1, y1)] for (x1, y1) in white_piece):
                    continue

                moves.append(('B', x, y, i, j))
            for (x, y) in white_piece:
                if white_piece[(x, y)] == 0:
                    continue
                if abs(i-x) != abs(j-y):
                    continue
                elif any(abs(i-x1) == abs(j-y1) and black_piece[(x1, y1)] for (x1, y1) in black_piece):
                    continue

                moves.append(('W', x, y, i, j))

    return moves


def swap(move, black_piece=black, white_piece=white):
    if move[0] == 'B':
        black_piece[(move[1], move[2])], black_piece[(move[3], move[4])] = \
            black_piece[(move[3], move[4])], black_piece[(move[1], move[2])]
    else:
        white_piece[(move[1], move[2])], white_piece[(move[3], move[4])] = \
            white_piece[(move[3], move[4])], white_piece[(move[1], move[2])]


def dfs_to_bfs():
    short_moves = []
    for move in get_valid_moves():
        swap(move)
        mask = hashed()
        if mask in pending:
            swap(move)
            continue
        pending.add(mask)
        short_moves.append(move)
        swap(move)
    return short_moves


def solve():
    tree = []
    node = [black.copy(), white.copy(), []]

    while 1:
        mask = hashed(node[0], node[1])
        # if len(node[2]) == 2 and ('W', 3, 4, 0, 1) in node[2]:
        #     print(node[2])
        #     display(node[0], node[1])

        if mask == goal:
            for x in node[2]:
                solution.append(x)
            return

        if not (mask in seen):
            seen.add(mask)
            for move in get_valid_moves(node[0], node[1]):
                new_black = node[0].copy()
                new_white = node[1].copy()
                swap(move, new_black, new_white)

                to_add = (new_black.copy(), new_white.copy(), node[2] + [move])

                tree.append(to_add)

        if len(tree):
            node = tree.pop(0)
        else:
            print('Not possible')
            return


def dfs_solve():
    # if len(solution) == 4:
    #     sys.exit()

    mask = hashed()
    is_goal = False
    if mask == goal:
        return True
    if mask in seen:
        return is_goal

    # print('Valid moves?: ', dfs_to_bfs())
    for move in dfs_to_bfs():

        solution.append(move)
        swap(move)

        # display()
        is_goal = dfs_solve()
        if is_goal:
            return True
        solution.pop()
        swap(move)

    return is_goal


display()
solve()
# print(*solution, sep='\n')
# print(len(solution))

for i in range(36):
    x = solution[i]
    print(i, x, sep='\n')
    swap(x)
    display()
