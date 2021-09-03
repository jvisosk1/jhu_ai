from main import *

X = 0
Y = 1

STATE = 0
COST = 1
PARENT = 2

COSTS = {'.': 1, '*': 3, '#': 5, '~': 7}
MOVES = [(0,-1), (1,0), (0,1), (-1,0)]


def get_successors(cur_state):
    successors = []

    for direction in MOVES:
        move = (cur_state[X] + direction[X], cur_state[Y] + direction[Y])

        # validation check that potential move in board realm
        if move[X] < 0 or move[X] >= len(test_world):
            continue
        elif move[Y] < 0 or move[Y] >= len(test_world):
            continue
        else:  # if move in bounds, append (move_coordinate, move_cost) to successor list
            move_key = test_world[move[X]][move[Y]]
            move_cost = COSTS[move_key]
            # print(f'cost of {move_key} = ', move_cost)
            successors.append((move, move_cost))

    # prioritize the successor list based on the cost of moves
    ranked_successors = sorted(successors, key=lambda x: x[1])

    # return only the move coordinate component of ranked_successors list (w/o cost)
    # return [x[0] for x in ranked_successors]
    return ranked_successors


def extract_path(explored):

    [print(i) for i in explored]

    explored.reverse()
    path = [explored[0][STATE]]
    next_node = explored[0][PARENT]

    for node in explored[1:]:
        if node[STATE] == next_node:
            # TODO: compare the costs of all nodes with parent state = node state
            path.append(node[STATE])
            next_node = node[PARENT]

    path.reverse()
    return path


def pretty_print_solution(path):

    for j in range(len(path)):
        cur_move = path[j]
        if j == len(path)-1:
            next_move = GOAL
        else: next_move = path[j+1]

        # if next move is downward
        if cur_move[X] < next_move[X]:
            test_world[cur_move[X]][cur_move[Y]] = 'v'

        # if next move is upward
        elif cur_move[X] > next_move[X]:
            test_world[cur_move[X]][cur_move[Y]] = '^'

        # if next move is right
        elif cur_move[Y] < next_move[Y]:
            test_world[cur_move[X]][cur_move[Y]] = '>'

        # if next move is left
        else: test_world[cur_move[X]][cur_move[Y]] = '<'

    test_world[GOAL[X]][GOAL[Y]] = 'G'

    for i in test_world:
        line = "".join(i)
        print(line.replace('.', '*').replace('~', '*').replace('#', '*'))

