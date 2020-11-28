import random

def make_level(colors):
    assert colors >= 2
    all_states = [[] for i in range(colors + 2)]
    print(all_states)
    for color in range(colors):
        balls = 0
        while balls < 4:
            tube = random.randint(0, colors - 1)
            if len(all_states[tube]) < 4:
                all_states[tube].append(color)
                balls += 1
    print(all_states)

make_level(0)