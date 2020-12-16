import random
import copy

PINK = 0
LIGHTGREEN = 1
DARKGREEN = 2
DARKBLUE = 3
LIGHTBLUE = 4
ORANGE = 5
PURPLE = 6
RED = 7
GREY = 8

COLORS = [PINK, PURPLE, LIGHTBLUE, LIGHTGREEN, DARKBLUE, DARKGREEN, RED, GREY, ORANGE]

def make_level(colors):
    assert len(COLORS) >= 2
    all_states = [[] for i in range(len(COLORS) + 2)]
    print(all_states)
    for color in COLORS:
        balls = 0
        while balls < 4:
            tube = random.randint(0, len(COLORS) - 1)
            if len(all_states[tube]) < 4:
                all_states[tube].append(color)
                balls += 1
    print(all_states)
    return all_states

def move_ball(tubes, start, goal):
    # assert len(tubes[start]) > 0
    # assert len(tubes[goal]) < 4
    # print(start, goal)
    ball = tubes[start].pop(-1)
    tubes[goal].append(ball)
    return tubes

def can_move_physically(tubes, start, goal):
    return len(tubes[start]) > 0 and len(tubes[goal]) < 4 and start != goal

def can_move_legally(tubes, start, goal):
    return len(tubes[goal]) == 0 or tubes[start][-1] == tubes[goal][-1]

def visited(tubes, states):
    return tubes in states

def can_move(tubes, start, goal, states):
    tubes_copy = copy.deepcopy(tubes)
    if can_move_physically(tubes, start, goal) and can_move_legally(tubes, start, goal):
        tubes_copy = move_ball(tubes_copy, start, goal)
        return not visited(sorted(tubes_copy), states)
    return False

def get_all_moves_from_tube(tubes, start, states):
    all_moves = []
    tubes_copy = copy.deepcopy(tubes)
    for goal in range(len(tubes)):
        if can_move(tubes, start, goal, states):
            move_ball(tubes_copy, start, goal)
            h = heuristic(tubes)
            all_moves.append((h, start, goal))
        tubes_copy = copy.deepcopy(tubes)   
    return all_moves

def get_all_moves(tubes, states):
    all_moves = []
    for start in range(len(tubes)):
        all_moves.extend(get_all_moves_from_tube(tubes, start, states))
    return all_moves

def game_over(tubes, states):
    return len(get_all_moves(tubes, states)) == 0

def complete(tube):
    if len(tube) == 0:
        return True
    if len(tube) != 4:
        return False
    for ball in range (1, 4):
        if tube[0] != tube[ball]:
            return False
    return True

def win(tubes):
    for tube in tubes:
        if not complete(tube):
            return False
    return True

def end_state(tubes, states):
    if win(tubes):
        print('WIN!')
        return True
    if game_over(tubes, states):
        print('GAME OVER!')
        return True
    return False

def heuristic_for_tube(tube):
    heuristic = 0
    if not complete(tube):
        lowest = tube[0]
        for ball in range (1, len(tube)):
            if ball != lowest:
                heuristic += len(tube) - ball
                break
    return heuristic
        
def heuristic(tubes):
    heuristic = 0
    for tube in tubes:
        heuristic += heuristic_for_tube(tube)

    tubes = sorted(tubes)

    heuristic += 2 * (len(tubes[0]) + len(tubes[1]))
    return heuristic

def solve(tubes):
    states = []
    while not win(tubes):
        tubes = copy.deepcopy(tubes_orig)
        states = []
        while not end_state(tubes, states):
            tubes_copy = copy.deepcopy(tubes)
            tubes_copy = sorted(tubes_copy)
            all_moves = get_all_moves(tubes, states)
            print(all_moves)
            move = all_moves[random.randint(0, len(all_moves) - 1)]
            print(move)
            tubes = move_ball(tubes, move[1], move[2])
            print(tubes) 
            states.append(tubes_copy)



# tubes = make_level(9)
tubes = [[LIGHTGREEN, DARKGREEN, LIGHTGREEN, DARKBLUE], [LIGHTGREEN, GREY, LIGHTBLUE, PURPLE], [LIGHTGREEN, PINK, PURPLE, PURPLE], [GREY, LIGHTBLUE, LIGHTBLUE, DARKGREEN], [PINK, DARKBLUE, GREY, DARKBLUE], [RED, GREY, RED, RED], [RED, PINK, PURPLE, ORANGE], [DARKGREEN, ORANGE, DARKBLUE, PINK], [DARKGREEN, ORANGE, ORANGE, LIGHTBLUE], [], []]
tubes_orig = copy.deepcopy(tubes)
print(tubes)
print(heuristic(tubes))
solve(tubes)
# while not win(tubes):
#     tubes = copy.deepcopy(tubes_orig)
#     states = []
#     while not end_state(tubes):
#         tubes_copy = copy.deepcopy(tubes)
#         tubes_copy = sorted(tubes_copy)
#         all_moves = get_all_moves(tubes, states)
#         print(all_moves)
#         move = all_moves[random.randint(0, len(all_moves) - 1)]
#         print(move)
#         tubes = move_ball(tubes, move[0], move[1])
#         print(tubes) 
#         states.append(tubes_copy)