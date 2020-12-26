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
CYAN = 9
MAGENTA = 10
BROWN = 11
WHITE = 12
BLACK = 13

COLORS = [PINK, LIGHTGREEN, DARKGREEN, DARKBLUE, LIGHTBLUE, ORANGE, PURPLE, RED, GREY, CYAN, MAGENTA, BROWN, WHITE, BLACK]

def make_level(level, colors):
    colors = colors[:level]

    assert len(colors) >= 2
    all_states = [[] for i in range(len(colors) + 2)]
    # all_states = tuple(all_states)
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
        return not visited(tubes_copy, states)
    return False

def get_all_moves_from_tube(tubes, start, states, c, search_set, previous):
    all_moves = []
    tubes_copy = copy.deepcopy(tubes)
    for goal in range(len(tubes)):
        cost = c
        if can_move(tubes_copy, start, goal, states):
            tubes_copy = move_ball(tubes_copy, start, goal)
            # tubes_sorted = sorted(tubes_copy)
            # if visited(tubes_sorted, states) and not searching(tubes_sorted, states):
            #     continue
            
            cost += 1
            h = heuristic(tubes_copy)
            f = h + cost
            move = {'f': f, 'h': h, 'start': start, 'goal': goal, 'tubes': copy.deepcopy(tubes), 'cost': cost, 'previous': previous}
            # search_set.add(copy.deepcopy(tuple(tubes_sorted)))
            all_moves.append(move)
        tubes_copy = copy.deepcopy(tubes)   
    return all_moves

def get_all_moves(tubes, states, c, search_set, previous):
    all_moves = []
    for start in range(len(tubes)):
        all_moves.extend(get_all_moves_from_tube(tubes, start, states, c, search_set, previous))
    return all_moves

def game_over(frontier, cost):
    return len(frontier) == 0 and cost != 0

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

def end_state(tubes, frontier, c):
    if win(tubes):
        print('WIN!')
        print("cost: ", c)
        return True
    if game_over(frontier, c):
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

    tubes_copy = copy.deepcopy(tubes)

    for count, tube in enumerate(tubes_copy):
        current = heuristic_for_tube(tube)
        tubes_copy[count] = list((tube, current))

    tubes_copy = sorted(tubes_copy)
    nb_empty = 0
    empty = True
    while empty:
        if len(tubes_copy[nb_empty][0]) == 0:
            nb_empty += 1
        else:
            empty = False
    
    tubes_copy = tubes_copy[nb_empty:]

    tubes_copy = sorted(sorted(tubes_copy, key=lambda x: len(x[0]) - x[1], reverse=True), key=lambda x: x[0][0])


    for count, tube in enumerate(tubes_copy):
        if count > 0 and tube[0][0] == tubes_copy[count - 1][0][0]:
            heuristic += len(tube[0])
        else:
            heuristic += tube[1]
    return heuristic

def searching(search, states):
    return search in states

def find_path(win_state):
    if win_state['previous'] == None:
        return [(win_state['start'], win_state['goal'])]
    
    else:
        return find_path(win_state['previous']) + [(win_state['start'], win_state['goal'])]
    


def solve(tubes):
    visited = []
    search_set = set()
    cost = 0
    frontier = []
    previous = None
    while not end_state(tubes, frontier, cost):
        tubes_copy = copy.deepcopy(tubes)
        all_moves = get_all_moves(tubes_copy, visited, cost, search_set, previous)
        frontier.extend(all_moves)
        frontier.sort(key=itemgetter('f'))
        frontier.sort(key=itemgetter('h'))
        best = frontier.pop(0)
        previous = best
        start = best['start']
        goal = best['goal']
        tubes = best['tubes']
        cost = best['cost']
        tubes = move_ball(tubes, start, goal)
        visited.append(tubes)

    return find_path(best)


