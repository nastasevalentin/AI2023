from queue import PriorityQueue
import time
import math

class EightPuzzleState:
    def __init__(self, board, empty_position, last_moved, parent=None):
        self.board = board
        self.empty_position = empty_position
        self.last_moved = last_moved
        self.parent = parent

    def is_goal(self):
        n = 1
        for row in self.board:
            for cell in row:
                if cell == 0:
                    continue
                if cell != n:
                    return False
                n = (n + 1) % 9
        return True

    def __lt__(self, other):
        return self.heuristic_value < other.heuristic_value

def is_valid_move(state, new_empty_position):
    x, y = state.empty_position
    if state.last_moved is not None:
        last_x, last_y = state.last_moved
    else:
        last_x, last_y = None, None

    return (0 <= new_empty_position[0] < 3 and 0 <= new_empty_position[1] < 3 and
            new_empty_position != (last_x, last_y) and
            (abs(new_empty_position[0] - x) + abs(new_empty_position[1] - y) == 1))


def get_neighbors(state):
    neighbors = []
    x, y = state.empty_position

    possible_moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    for new_x, new_y in possible_moves:
        if is_valid_move(state, (new_x, new_y)):
            new_board = [list(row) for row in state.board]
            new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
            new_empty_position = (new_x, new_y)
            neighbors.append(EightPuzzleState(new_board, new_empty_position, (x, y)))

    return neighbors


def depth_limited_DFS(state, depth, visited, move_counter):
    if state.is_goal():
        return state
    if depth == 0:
        return None
    visited.add(state)
    for neighbor in get_neighbors(state):
        if neighbor not in visited:
            move_counter[0] += 1
            res = depth_limited_DFS(neighbor, depth - 1, visited, move_counter)
            if res is not None:
                return res
            move_counter[0] -= 1

def iddfs(init_state, max_depth):
    move_counter = [0]

    for depth in range(max_depth + 1):
        visited = set()
        sol = depth_limited_DFS(init_state, depth, visited, move_counter)
        if sol is not None:
            return sol, move_counter[0], depth
    return None, 0

def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = state.board[i][j]
            if tile != 0:
                goal_x, goal_y = (tile - 1) // 3, (tile - 1) % 3
                distance += abs(i - goal_x) + abs(j - goal_y)
    state.heuristic_value = distance
    return distance


def hamming_distance(state):
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != 0 and state.board[i][j] != 3 * i + j + 1:
                misplaced_tiles += 1
    state.heuristic_value = misplaced_tiles
    return misplaced_tiles

def run_iddfs(initial_state, max_depth):
    start_time = time.time()
    solution, num_moves, depth = iddfs(initial_state, max_depth)
    end_time = time.time()
    return solution, num_moves, depth, end_time - start_time

def run_greedy(initial_state, heuristic_func):
    start_time = time.time()
    pq = PriorityQueue()
    pq.put((heuristic_func(initial_state), 0, initial_state))
    visited = set()
    while not pq.empty():
        _, depth, state = pq.get()

        if state.is_goal():
            final_state = state.board
            num_moves = 0
            while state is not None:
                num_moves += 1
                state = state.parent
            num_moves -= 1
            return state, final_state,num_moves, time.time() - start_time

        visited.add(state)

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                neighbor.parent = state
                pq.put((heuristic_func(neighbor), depth + 1, neighbor))

    return None, 0, time.time() - start_time

def chebyshev_distance(state):
    max_distance = 0
    for i in range(3):
        for j in range(3):
            tile = state.board[i][j]
            if tile != 0 and tile != 3 * i + j + 1:
                goal_x, goal_y = (tile - 1) // 3, (tile - 1) % 3
                dx = abs(i - goal_x)
                dy = abs(j - goal_y)
                max_distance = max(max_distance, dx, dy)
    state.heuristic_value = max_distance
    return max_distance

initial_state1 = EightPuzzleState([[2, 5, 3], [1, 0, 6], [4, 7, 8]], (1, 1), None)
initial_state2 = EightPuzzleState([[8, 6, 7], [2, 5, 4], [0, 3, 1]], (2, 0), None)
initial_state3 = EightPuzzleState([[2, 7, 5], [0, 8, 4], [3, 1, 6]], (0, 1), None)

max_depth = 30
num_moves3 = 0
solution1, final_state1, num_moves1, exec_time1 = run_greedy(initial_state1, hamming_distance)
solution2, final_state2, num_moves2, exec_time2 = run_greedy(initial_state2, chebyshev_distance)
solution3, final_state3, num_moves3, exec_time3 = run_greedy(initial_state3, manhattan_distance)
solution, depth, num_moves, exec_time = run_iddfs(initial_state3, max_depth)

print("IDDFS")
if solution is not None:
    print("Solution found:")
    for row in solution.board:
        print(row)
    print("Solution Length:", num_moves)
    print("Execution Time:", exec_time)
else:
    print("No solution found.")


print("\nHAMMING GREEDY")
if final_state1 is not None:
    print("Solution found:")
    for row in final_state1:
        print(row)
    print("Solution Length:", num_moves1)
    print("Execution Time:", exec_time1)
else:
    print("No solution found.")


print("\nCHEBYSHEV GREEDY")
if final_state2 is not None:
    print("Solution found:")
    for row in final_state2:
        print(row)
    print("Solution Length:", num_moves2)
    print("Execution Time:", exec_time2)
else:
    print("No solution found.")


print("\nMANHATTAN GREEDY")
if final_state3 is not None:
    print("Solution found:")
    for row in final_state3:
        print(row)
    print("Solution Length:", num_moves3)
    print("Execution Time:", exec_time3)
else:
    print("No solution found.")


