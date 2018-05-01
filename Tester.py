import json
from timeit import timeit

# with open("Chinese_checkers/test_game_states.json") as file:
#     data = json.load(file)
#     data["heuristic"] = True
# with open("Chinese_checkers/test_game_states.json", "w") as file:
#     json.dump(data, file)
# print("With heuristics", timeit("checkers_AI.dfs_solve()", setup="from Chinese_checkers import checkers_AI", number=1))
# with open("Chinese_checkers/test_game_states.json") as file:
#     data = json.load(file)
#     data["heuristic"] = False
# with open("Chinese_checkers/test_game_states.json", "w") as file:
#     json.dump(data, file, indent=1)
print("No heuristic", timeit("checkers_AI.dfs_solve()", setup="from Chinese_checkers import checkers_AI", number=1))
