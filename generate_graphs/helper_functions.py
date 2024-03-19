from itertools import permutations

def generate_combinations(actions):
    combinations = []
    for i in range(1, len(actions) + 1):
        for perm in permutations(actions, i):
            combinations.append(','.join(perm))
    return combinations