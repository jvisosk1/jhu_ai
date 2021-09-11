from utils import *

START = (0,0)
GOAL = (6,6)

test_world = [
  ['.', '*', '*', '*', '#', '#', '#'],  # row 0
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '.', '.', '.', '.', '.', '.'],  # row 3
  ['*', '*', '*', '*', '*', '*', '.'],
  ['*', '*', '*', '*', '*', '*', '.'],
  ['~', '~', '~', '*', '*', '*', '.'],  # row 6
]


def heuristic(cur_state, goal_state):
    h_value = abs(cur_state[X] - goal_state[X]) + abs(cur_state[Y] - goal_state[Y])
    return h_value


def a_star_search(start, goal, costs, moves):
    frontier = [(start, 1, None, heuristic(start, goal))]
    explored = {}

    while len(frontier) > 0:
        cur = frontier[0]

        children = get_successors(cur[STATE])

        # for each successor/child attach to node: cost from start, current state, and heuristic cost + cost from start
        children = [
            (child[STATE], child[COST] + cur[COST], cur[STATE], child[COST] + cur[COST] + heuristic(child[STATE], goal))
            for child in children
        ]

        if cur[STATE] == goal:
            explored[cur[STATE]] = [cur[COST], cur[PARENT]]
            return explored

        frontier.remove(cur)

        # add children to frontier if not on explored or frontier lists
        [frontier.append(child) for child in children if (child[STATE] not in explored and child not in frontier)]

        # sort the frontier list by f(n) where f(n) = g(n) + h(n)
        frontier = sorted(frontier, key=lambda x: x[HEURISTIC_PLUS_TOTAL_COST])

        # add current state to explored, or if dict key (current state) already exists replace if current cost is less
        if (cur[STATE] not in explored) or (cur[COST] < explored.get(cur[STATE])[0]):
            explored[cur[STATE]] = [cur[COST], cur[PARENT]]

    return None


if __name__ == '__main__':

    # for i in range(len(test_world[0])):
    #     for j in range(len(test_world)):
    #         goal = (i,j)
    #         print('GOAL:', goal)
    #         explored = a_star_search(START, goal, COSTS, MOVES)
    #         path = extract_path(explored, goal)
    #         print(path)
    #         pretty_print_solution(path, goal)

    explored = a_star_search(START, GOAL, COSTS, MOVES)
    path, rel_path = extract_path(explored, GOAL)
    print(path)
    print(rel_path)
    pretty_print_solution(path, GOAL)