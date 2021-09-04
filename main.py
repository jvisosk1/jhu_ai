from utils import *

START = (0,0)
GOAL = (6,5)

test_world = [
  ['.', '*', '*', '*', '#', '#', '#'],  # row 0
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '.', '.', '.', '.', '.', '.'],  # row 3
  ['*', '*', '*', '*', '*', '*', '.'],
  ['*', '*', '*', '*', '*', '*', '.'],
  ['~', '~', '~', '*', '*', '*', '.'],  # row 6
]


def heuristic_cost(cur_state, goal_state):
    h_value = abs(cur_state[X] - goal_state[X]) + abs(cur_state[Y] - goal_state[Y])
    print(f'h() of {cur_state} and goal {goal_state} = {h_value}')
    return abs(cur_state[X] - goal_state[X]) + abs(cur_state[Y] - goal_state[Y])


def a_star_search(start, goal, costs, moves):
    frontier = [(start, 1, None)]
    explored = {}

    while len(frontier) > 0:
        current_state = frontier[0]
        current_cost = current_state[COST]

        children = get_successors(current_state[STATE])
        children = [
            # (child[STATE], child[COST] + current_cost + heuristic_cost(child[STATE], goal), current_state[STATE])
            (child[STATE], child[COST] + current_cost, current_state[STATE])
            for child in children
        ]

        if current_state[STATE] == goal:
            explored[current_state[STATE]] = [current_state[COST], current_state[PARENT]]
            return explored

        # add children to frontier if not on explored or frontier lists
        [frontier.append(child) for child in children if (child[STATE] not in explored and child not in frontier)]
        frontier = sorted(frontier, key=lambda x: x[1])
        frontier.remove(current_state)

        if (current_state[STATE] not in explored) or (current_state[COST] < explored.get(current_state[STATE])[0]):
            explored[current_state[STATE]] = [current_state[COST], current_state[PARENT]]

    return None


if __name__ == '__main__':

    for i in range(len(test_world[0])):
        for j in range(len(test_world)):
            goal = (i,j)
            print('GOAL:', goal)
            explored = a_star_search(START, goal, COSTS, MOVES)
            path = extract_path(explored, goal)
            print(path)
            pretty_print_solution(path, goal)

    # explored = a_star_search(START, GOAL, COSTS, MOVES)
    # path = extract_path(explored, GOAL)
    # pretty_print_solution(path, GOAL)
