import main

def actual_tests():
    level = 4

    tubes = main.make_level(level, main.COLORS)

    assert len(tubes) == level + 2
    for tube in tubes[:4]:
        assert len(tube) == 4

    for tube in tubes[4:]:
        assert len(tube) == 0

    print("make_level() OK")

    tubes = [[0, 0, 3, 5], [2, 3, 4, 5], [0, 1, 1, 2], [0, 1, 2, 3], [3, 4, 4, 5], [1, 2, 4, 5], [], []]

    for tube in tubes:
        assert main.heuristic_for_tube(tube) <= 3

    assert main.heuristic(tubes) == 17

    print("heuristic() OK")

    assert not main.can_move(tubes, 0, 0, [])
    assert not main.can_move(tubes, 0, 1, [])
    assert main.can_move(tubes, 0, 6, [])

    print("can_move OK")

    assert main.visited(tubes, [tubes])

    print("visited OK")

    tubes = main.move_ball(tubes, 0, 6)

    assert tubes == [[0, 0, 3], [2, 3, 4, 5], [0, 1, 1, 2], [0, 1, 2, 3], [3, 4, 4, 5], [1, 2, 4, 5], [5], []]

#TODO make more robust, not feeling like doing so right now, might do while debugging

tubes = [[main.ORANGE, main.LIGHTGREEN, main.RED, main.PINK], [main.DARKBLUE, main.DARKBLUE, main.LIGHTBLUE, main.PINK], 
[main.RED, main.PURPLE, main.LIGHTGREEN, main.LIGHTBLUE], [main.PINK, main.GREY, main.ORANGE, main.GREY], [main.LIGHTBLUE, main.GREY, main.DARKGREEN, main.PINK], 
[main.RED, main.ORANGE, main.LIGHTGREEN, main.GREY], [main.RED, main.DARKBLUE, main.PURPLE, main.ORANGE], [main.DARKBLUE, main.PURPLE, main.DARKGREEN, main.PURPLE], 
[main.LIGHTBLUE, main.LIGHTGREEN, main.DARKGREEN, main.DARKGREEN], [], []]
# tubes = main.make_level(14, main.COLORS)

# print(main.heuristic(tubes))
print(main.solve(tubes))


