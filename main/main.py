import random
import copy
from operator import itemgetter

PINK = 0
LIGHTGREEN = 1
DARKGREEN = 2
DARKBLUE = 3
LIGHTBLUE = 4
ORANGE = 5
PURPLE = 6
RED = 7
GREY = 8

COLORS = [PINK, LIGHTGREEN, DARKGREEN, DARKBLUE, LIGHTBLUE, ORANGE, PURPLE, RED, GREY]

def make_level(level, colors):
    colors = colors[:level]

    assert len(colors) >= 2
    all_states = [[] for i in range(len(colors) + 2)]
    print(all_states)
    for color in colors:
        balls = 0
        while balls < 4:
            tube = random.randint(0, len(colors) - 1)
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
    return tubes in states # actual snipping could be added but the heuristic used is consistent and admissable so it's not necessary and would only make things more complicated, this is more elegant

def can_move(tubes, start, goal, states):
    tubes_copy = copy.deepcopy(tubes)
    if can_move_physically(tubes, start, goal) and can_move_legally(tubes, start, goal):
        tubes_copy = move_ball(tubes_copy, start, goal)
        return not visited(sorted(tubes_copy), states)
    return False

def get_all_moves_from_tube(tubes, start, states, c):
    all_moves = []
    tubes_copy = copy.deepcopy(tubes)
    for goal in range(len(tubes)):
        cost = c
        if can_move(tubes_copy, start, goal, states):
            tubes_copy = move_ball(tubes_copy, start, goal)
            cost += 1
            h = heuristic(tubes_copy)
            f = h + cost
            move = {'f': f, 'h': h, 'start': start, 'goal': goal, 'tubes': copy.deepcopy(tubes), 'cost': cost} #TODO fix same tubes_copy being altered (might have to solve this recursively)
            all_moves.append(move)
        tubes_copy = copy.deepcopy(tubes)   
    return all_moves

def get_all_moves(tubes, states, c):
    all_moves = []
    for start in range(len(tubes)):
        all_moves.extend(get_all_moves_from_tube(tubes, start, states, c))
    all_moves.sort(key=itemgetter('h'))
    all_moves.sort(key=itemgetter('f'))
    return all_moves

# def game_over(frontier, cost):
#     return len(frontier) == 0 and cost != 0

def game_over(tubes, states, c):
    return len(get_all_moves(tubes, states, c)) == 0

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

# def end_state(tubes, frontier, c):
def end_state(tubes, states, c):
    if win(tubes):
        print('WIN!')
        print("cost: ", c)
        return True
    # if game_over(frontier, c):
    if game_over(tubes, states, c):
        print('GAME OVER!')
        return True
    return False

def heuristic_for_tube(tube):
    heuristic = 0
    if not complete(tube):
        lowest = tube[0]
        for ball in range (1, len(tube)):
            if tube[ball] != lowest:
                heuristic += len(tube) - ball
                break
    return heuristic
        
def heuristic(tubes):
    heuristic = 0
    for tube in tubes:
        heuristic += heuristic_for_tube(tube)

    tubes = sorted(tubes, key=len)

    heuristic += (len(tubes[0]) + len(tubes[1]))
    return heuristic

def solve(tubes):
    print(tubes)
    visited = []
    cost = 0
    frontier = []
    while not end_state(tubes, frontier, cost):
        tubes_copy = copy.deepcopy(tubes)
        tubes_copy = sorted(tubes_copy)
        all_moves = get_all_moves(tubes, visited, cost)
        frontier.extend(all_moves)
        frontier.sort(key=itemgetter('h'))
        frontier.sort(key=itemgetter('f'))
        # print(frontier)
        best = frontier.pop(0)
        print(best)
        start = best['start']
        goal = best['goal']
        tubes = best['tubes']
        cost = best['cost']
        print(start, goal)
        tubes = move_ball(tubes, start, goal)
        print(tubes) 
        visited.append(tubes)

def solve_recursive(tubes, c, visited):
    print(tubes)
    frontier = []
    while not end_state(tubes, frontier, c):
        tubes_copy = copy.deepcopy(tubes)
        tubes_copy = sorted(tubes_copy)
        all_moves = get_all_moves(tubes, visited, c)
        frontier.extend(all_moves)
        frontier.sort(key=itemgetter('f'))
        print(frontier)
        best = frontier.pop(0)
        print(best)
        start = best['start']
        goal = best['goal']
        tubes = best['tubes']
        c = best['cost']
        print(start, goal)
        tubes = move_ball(tubes, start, goal)
        print(tubes) 
        visited.append(tubes)


#TODO rework solver for A* instead of random search
#TODO recursive?
