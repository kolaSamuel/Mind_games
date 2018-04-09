from copy import deepcopy


def play():
    depth = [2 ]
    game_state = open('GameState.txt', 'r')
    around = [[0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1]]
    step = [[0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -2], [-2, -2], [-2, 0], [-2, 2],
            [0, 2], [2, 2], [2, 0], [2, -2]]
    minimax = [(-1 ** i) * float('inf') for i in xrange(depth[0] + 1)]
    positions = {0: set(), 1: set(), 2: set()}

    for i in xrange(6):
        row = map(int, game_state.readline().split())
        for j in xrange(6):
            positions[row[j]].add((i, j))
    game_state.close()

    def dfs(s,level=1):
        idx = ((level) % 2) + 1
        if level > depth[0]:
            return
        for r1, c1 in s[idx]:
            for r, c in step:
                r2, c2 = [r1 + r, c1 + c]
                arr = deepcopy(s)
                arr = move(arr, r1, c1, r2, c2, idx)
                if arr == s:
                    continue
                #else: print arr[1]
                dfs(arr, level + 1)
                if idx == 2:
                    maxi(arr, level, [r1, c1, r2, c2])
                else:
                    mini(arr, level)

    def maxi(arr, level, moves):
        if len(arr[2]) > minimax[level]:
            minimax[level] = len(arr[1])
            if level == 1:
                minimax[0] = moves

    def mini(arr, level):
        minimax[level] = min(minimax[level], len(arr[2]))

    def move(arr, r1, c1, r2, c2, idx):
        # arr = u.copy()
        if (r2, c2) not in arr[0]:
            return arr
        else:
            return possible_move(arr, r1, c1, r2, c2, idx)

    def possible_move(arr, r1, c1, r2, c2, idx):
        tot = [r1, c1, r2, c2]
        diff = [abs(r2 - r1), abs(c2 - c1)]
        if min(tot) < 0 or max(tot) > 5:
            return arr
        elif max(diff) == 1:
            arr[idx].add((r2, c2))
            arr[0].remove((r2, c2))
        elif max(diff) == 2:
            arr[idx].add((r2, c2))
            arr[idx].remove((r1, c1))
        return change(arr, idx, r2, c2)

    def change(arr, idx, r2, c2):
        for i, j in around:
            r3, c3 = [r2 + i, c2 + j]
            if min(r3, c3) < 0 or max(r3, c3) > 5: continue
            other = (idx % 2) + 1
            if (r3, c3) in arr[other]:
                arr[other].remove((r3, c3))
                arr[idx].add((r3, c3))
        return arr

    dfs(positions)
    # change the text file
    ans = minimax[0]
    r1, c1, r2, c2 = ans
    positions = move(positions, r1, c1, r2, c2, 2)
    rewrite = open('GameState.txt', 'w')
    arr = [[0] * 6 for _ in xrange(6)]
    for i in xrange(1,3):
        for r, c in positions[i]:
            arr[r][c] = i
    for i in xrange(6):
        print >> rewrite, " ".join(map(str, arr[i]))
    rewrite.close()