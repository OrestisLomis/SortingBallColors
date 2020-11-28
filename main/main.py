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
    return all_states

def move_ball(tubes, start, goal):
    # assert len(tubes[start]) > 0
    # assert len(tubes[goal]) < 4

    if len(tubes[start]) > 0 and len(tubes[goal]) < 4:
        ball = tubes[start].pop(-1)
        tubes[goal].append(ball)
    return tubes

states = make_level(4)
for i in range(20):
    start = random.randint(0, 5)
    goal = random.randint(0, 5)
    states = move_ball(states, start, goal)
    print(states)

