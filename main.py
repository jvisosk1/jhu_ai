from utils import *

START = (0,0)
GOAL = (0,5)




test_world = [
  ['.', '*', '*', '*', '#', '#', '#'],  # row 0
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '.', '.', '.', '.', '.', '.'],  # row 3
  ['*', '*', '*', '*', '*', '*', '.'],
  ['*', '*', '*', '*', '*', '*', '.'],
  ['~', '~', '~', '*', '*', '*', '.'],  # row 6
]


def a_star_search(world, start, goal, costs, moves):
    frontier = [(start, 1, None)]
    explored = []
    explored_states = []

    while len(frontier) > 0:
        current_state = frontier[0]
        current_cost = current_state[COST]
        # print('cost:', current_cost)

        # print('CURRENT STATE:', current_state)

        children = get_successors(current_state[STATE])
        children = [(child[STATE], child[COST] + current_cost, current_state[STATE]) for child in children]
        # print('successors:', children)

        if current_state[STATE] == goal:
            print('\n*************\nGOAL REACHED!\n*************')
            explored.append(current_state)
            print('TOTAL PATH COST:', current_cost)
            return explored

        # add children to frontier if not on explored or frontier lists
        [frontier.append(child) for child in children if (child[STATE] not in explored_states and child not in frontier)]
        frontier = sorted(frontier, key=lambda x: x[1])

        frontier.remove(current_state)
        explored_states.append(current_state[STATE])
        explored.append(current_state)

        # print('frontier:  ', frontier)
        # print('explored:  ', explored, '\n')

    return None


if __name__ == '__main__':
    path = a_star_search(test_world, START, GOAL, COSTS, MOVES)
    path = extract_path(path)
    pretty_print_solution(path)
