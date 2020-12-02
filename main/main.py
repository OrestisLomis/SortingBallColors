import random
import copy

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
    for goal in range(len(tubes)):
        if can_move(tubes, start, goal, states):
            all_moves.append((start, goal))
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

def end_state(tubes):
    if win(tubes):
        print('WIN!')
        return True
    if game_over(tubes, states):
        print('GAME OVER!')
        return True
    return False


tubes = make_level(9)
tubes_orig = copy.deepcopy(tubes)
states = list()
while not win(tubes):
    tubes = copy.deepcopy(tubes_orig)
    states = []
    while not end_state(tubes):
        tubes_copy = copy.deepcopy(tubes)
        tubes_copy = sorted(tubes_copy)
        all_moves = get_all_moves(tubes, states)
        print(all_moves)
        move = all_moves[random.randint(0, len(all_moves) - 1)]
        print(move)
        tubes = move_ball(tubes, move[0], move[1])
        print(tubes) 
        states.append(tubes_copy)