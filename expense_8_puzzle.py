import sys
from datetime import datetime
from collections import deque
import heapq


VERBOSE = False

def log(message, dump_flag, log_file):
    if dump_flag and log_file:
        with open(log_file, 'a') as fp:
            fp.write(message + '\n')

def read_puzzle(filename: str):
    """
    Read the puzzle from a file

    :param filename:
    :return:
    """
    with open(filename, 'r') as f:
        puzzle = []
        for line in f:
            if "END" in line:
                break
            puzzle.append([int(x) for x in line.split()])
        return puzzle

def heuristic(state: list, goal: list):
    """
    Manhattan distance heuristic modified to include tile cost

    :param state:
    :param goal:
    :return:
    """
    cost = 0
    for i in range(3):
        for j in range(3):
            tile = state[i][j]
            if tile != 0:  # skip the blank tile
                goal_i, goal_j = [(x, y) for x in range(3) for y in range(3) if goal[x][y] == tile][0]
                cost += tile * (abs(i - goal_i) + abs(j - goal_j))
    return cost

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = depth

    def __lt__(self, other):
        return self.cost < other.cost

def is_goal(state: list, goal: list):
    """
    Check if the state is the goal state

    :param state:
    :param goal:
    :return:
    """
    return state == goal

def get_successors(node, goal: list):
    """
    Get possible moves for the blank tile (0)

    :param node:
    :param goal:
    :return:
    """
    state = node.state
    moves = []
    blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
    directions = [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]

    for di, dj, direction in directions:
        new_i, new_j = blank_i + di, blank_j + dj
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = [row[:] for row in state]
            tile = new_state[new_i][new_j]
            new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
            moves.append(Node(new_state, node, f"Move {tile} {direction}", node.cost + tile, node.depth + 1))

    return moves

# A* search algorithm
def a_star(start, goal, dump_flag=False, log_file=None):
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, (heuristic(start, goal), 0, Node(start)))
    nodes_popped = nodes_expanded = nodes_generated = 0
    max_fringe_size = 1

    while open_list:
        _, _, current_node = heapq.heappop(open_list)
        nodes_popped += 1

        log(f"\nPopping node: {current_node.state}, g(n) = {current_node.cost}, depth = {current_node.depth}", dump_flag, log_file)

        if is_goal(current_node.state, goal):
            log(f"\nGoal state reached: {current_node.state}", dump_flag, log_file)
            return current_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

        closed_set.add(tuple(map(tuple, current_node.state)))
        nodes_expanded += 1

        for successor in get_successors(current_node, goal):
            if tuple(map(tuple, successor.state)) in closed_set:
                continue

            heapq.heappush(open_list, (successor.cost + heuristic(successor.state, goal), successor.depth, successor))
            nodes_generated += 1

        max_fringe_size = max(max_fringe_size, len(open_list))

        log(f"Fringe: {[node.state for _, _, node in open_list]}", dump_flag, log_file)
        log(f"Nodes expanded: {nodes_expanded}, Nodes generated: {nodes_generated}, Max fringe size: {max_fringe_size}", dump_flag, log_file)

    log("No solution found.", dump_flag, log_file)
    return None, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

def ucs(start, goal, dump_flag=False, log_file='/dev/null'):
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, (0, Node(start)))  # Priority queue sorted by g(n)
    nodes_popped, nodes_expanded, nodes_generated = 0, 0, 0
    max_fringe_size = 1

    while open_list:
        current_cost, current_node = heapq.heappop(open_list)  # Pop the least cost node
        nodes_popped += 1

        log(f"\nPopping node: {current_node.state}, g(n) = {current_node.cost}, depth = {current_node.depth}", dump_flag, log_file)

        if is_goal(current_node.state, goal): # Check if we reached the goal
            log(f"\nGoal state reached: {current_node.state}", dump_flag, log_file)
            return current_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

        closed_set.add(tuple(map(tuple, current_node.state)))
        nodes_expanded += 1

        log(f"Closed set: {list(closed_set)}", dump_flag, log_file)

        for successor in get_successors(current_node, goal): # Generate successors (neighboring states)
            if tuple(map(tuple, successor.state)) in closed_set:
                continue

            heapq.heappush(open_list, (successor.cost, successor))  # Priority by g(n) = successor.cost
            nodes_generated += 1

        max_fringe_size = max(max_fringe_size, len(open_list))  # Update max fringe size

        log(f"Fringe: {[node.state for _, node in open_list]}", dump_flag, log_file)
        log(f"Nodes expanded: {nodes_expanded}, Nodes generated: {nodes_generated}, Max fringe size: {max_fringe_size}", dump_flag, log_file)

    log("No solution found.", dump_flag, log_file)
    return None, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size



def bfs(start, goal, dump_flag=False, log_file=None):
    open_list = deque([Node(start)])  # Use a queue for BFS
    closed_set = set()
    nodes_popped, nodes_expanded, nodes_generated = 0, 0, 0
    max_fringe_size = 1

    while open_list:
        current_node = open_list.popleft()  # Pop from the left (FIFO)
        nodes_popped += 1

        log(f"\nPopping node: {current_node.state}, g(n) = {current_node.cost}, depth = {current_node.depth}", dump_flag, log_file)

        if is_goal(current_node.state, goal):  # Check if we reached the goal
            log(f"\nGoal state reached: {current_node.state}", dump_flag, log_file)
            return current_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

        closed_set.add(tuple(map(tuple, current_node.state)))
        nodes_expanded += 1

        log(f"Closed set: {list(closed_set)}", dump_flag, log_file)

        # Generate successors (neighboring states)
        for successor in get_successors(current_node, goal):
            if tuple(map(tuple, successor.state)) in closed_set:
                continue

            open_list.append(successor)  # Append to the right (FIFO)
            nodes_generated += 1

        max_fringe_size = max(max_fringe_size, len(open_list))

        log(f"Fringe: {[node.state for node in open_list]}", dump_flag, log_file)
        log(f"Nodes expanded: {nodes_expanded}, Nodes generated: {nodes_generated}, Max fringe size: {max_fringe_size}", dump_flag, log_file)

    log("No solution found.", dump_flag, log_file)
    return None, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

def dfs(start, goal, dump_flag=False, log_file='/dev/null'):
    open_list = [Node(start)]  # Use a stack for DFS (LIFO)
    closed_set = set()
    nodes_popped, nodes_expanded, nodes_generated = 0, 0, 0
    max_fringe_size = 1

    while open_list:
        current_node = open_list.pop()  # Pop from the right (LIFO)
        nodes_popped += 1

        log(f"\nPopping node: {current_node.state}, g(n) = {current_node.cost}, depth = {current_node.depth}", dump_flag, log_file)

        if is_goal(current_node.state, goal):  # Check if we reached the goal
            log(f"\nGoal state reached: {current_node.state}", dump_flag, log_file)
            return current_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

        closed_set.add(tuple(map(tuple, current_node.state)))
        nodes_expanded += 1

        log(f"Closed set: {list(closed_set)}", dump_flag, log_file)

        for successor in get_successors(current_node, goal): # Generate successors (neighboring states)
            if tuple(map(tuple, successor.state)) in closed_set:
                continue

            open_list.append(successor)  # Append to the stack (LIFO)
            nodes_generated += 1

        max_fringe_size = max(max_fringe_size, len(open_list))

        log(f"Fringe: {[node.state for node in open_list]}", dump_flag, log_file)
        log(f"Nodes expanded: {nodes_expanded}, Nodes generated: {nodes_generated}, Max fringe size: {max_fringe_size}", dump_flag, log_file)

    log("No solution found.", dump_flag, log_file)
    return None, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

def dls(start, goal, dump_flag=False, log_file='/dev/null'):
    depth_limit = int(input("Enter depth limit: "))  # Get depth limit from user input

    open_list = [Node(start)]  # Use a stack for DLS (LIFO)
    closed_set = set()
    nodes_popped, nodes_expanded, nodes_generated = 0, 0, 0
    max_fringe_size = 1

    while open_list:
        current_node = open_list.pop()  # Pop from the right (LIFO)
        nodes_popped += 1

        log(f"\nPopping node: {current_node.state}, g(n) = {current_node.cost}, depth = {current_node.depth}", dump_flag, log_file)

        if is_goal(current_node.state, goal): # Check if we reached the goal
            log(f"\nGoal state reached: {current_node.state}", dump_flag, log_file)
            return current_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

        if current_node.depth >= depth_limit: # If the current node's depth exceeds the depth limit, don't expand further
            continue

        closed_set.add(tuple(map(tuple, current_node.state)))
        nodes_expanded += 1

        log(f"Closed set: {list(closed_set)}", dump_flag, log_file)

        for successor in get_successors(current_node, goal): # Generate successors (neighboring states)
            if tuple(map(tuple, successor.state)) in closed_set:
                continue

            open_list.append(successor)  # Append to the stack (LIFO)
            nodes_generated += 1

        max_fringe_size = max(max_fringe_size, len(open_list))

        log(f"Fringe: {[node.state for node in open_list]}", dump_flag, log_file)
        log(f"Nodes expanded: {nodes_expanded}, Nodes generated: {nodes_generated}, Max fringe size: {max_fringe_size}", dump_flag, log_file)

    log("No solution found.", dump_flag, log_file)
    return None, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

def ids(start, goal, dump_flag=False, log_file='/dev/null'):
    nodes_popped_total, nodes_expanded_total, nodes_generated_total = 0, 0, 0
    max_fringe_size_total = 0
    depth_limit = 0  # Start with a depth limit of 0

    while True:
        result, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size = dls_with_limit(
            start, goal, depth_limit, dump_flag, log_file
        )

        nodes_popped_total += nodes_popped
        nodes_expanded_total += nodes_expanded
        nodes_generated_total += nodes_generated
        max_fringe_size_total = max(max_fringe_size_total, max_fringe_size)

        if result is not None:
            return result, nodes_popped_total, nodes_expanded_total, nodes_generated_total, max_fringe_size_total

        depth_limit += 1  # Increase depth limit if goal not found
        log(f"\nIncreasing depth limit to {depth_limit}\n", dump_flag, log_file)

def dls_with_limit(start, goal, depth_limit, dump_flag=False, log_file='/dev/null'):
    open_list = [Node(start)]  # Stack for depth-limited search
    closed_set = set()
    nodes_popped, nodes_expanded, nodes_generated = 0, 0, 0
    max_fringe_size = 1

    while open_list:
        current_node = open_list.pop()  # Pop from the right (LIFO)
        nodes_popped += 1

        log(f"\nPopping node: {current_node.state}, g(n) = {current_node.cost}, depth = {current_node.depth}", dump_flag, log_file)

        if is_goal(current_node.state, goal):  # Check if we reached the goal
            log(f"\nGoal state reached: {current_node.state}", dump_flag, log_file)
            return current_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

        if current_node.depth >= depth_limit:  # Stop expanding if depth limit exceeded
            continue

        closed_set.add(tuple(map(tuple, current_node.state)))
        nodes_expanded += 1

        log(f"Closed set: {list(closed_set)}", dump_flag, log_file)

        for successor in get_successors(current_node, goal): # Generate successors (neighboring states)
            if tuple(map(tuple, successor.state)) in closed_set:
                continue

            open_list.append(successor)  # Append to stack (LIFO)
            nodes_generated += 1

        max_fringe_size = max(max_fringe_size, len(open_list))  # Update max fringe size

        log(f"Fringe: {[node.state for node in open_list]}", dump_flag, log_file)
        log(f"Nodes expanded: {nodes_expanded}, Nodes generated: {nodes_generated}, Max fringe size: {max_fringe_size}", dump_flag, log_file)

    return None, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

def greedy_search(start, goal, dump_flag=False, log_file='/dev/null'):
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, (heuristic(start, goal), Node(start)))  # Priority queue sorted by h(n)
    nodes_popped, nodes_expanded, nodes_generated = 0, 0, 0
    max_fringe_size = 1


    log(f"Command-Line Arguments: ['start.txt', 'goal.txt', 'greedy', '{dump_flag}']", dump_flag, log_file)
    log("Method Selected: greedy", dump_flag, log_file)

    while open_list:
        _, current_node = heapq.heappop(open_list)  # Pop the node with the lowest h(n)
        nodes_popped += 1

        log(f"\nPopping node: {current_node.state}, h(n) = {heuristic(current_node.state, goal)}, depth = {current_node.depth}", dump_flag, log_file)

        # Check if we reached the goal
        if is_goal(current_node.state, goal):
            log(f"\nGoal state reached: {current_node.state}", dump_flag, log_file)
            return current_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

        closed_set.add(tuple(map(tuple, current_node.state)))
        nodes_expanded += 1

        log(f"Closed set: {list(closed_set)}", dump_flag, log_file)

        for successor in get_successors(current_node, goal): # Generate successors (neighboring states)
            if tuple(map(tuple, successor.state)) in closed_set:
                continue

            heapq.heappush(open_list, (heuristic(successor.state, goal), successor))  # Prioritize based on h(n)
            nodes_generated += 1

        max_fringe_size = max(max_fringe_size, len(open_list))

        log(f"Fringe: {[node.state for _, node in open_list]}", dump_flag, log_file)
        log(f"Nodes expanded: {nodes_expanded}, Nodes generated: {nodes_generated}, Max fringe size: {max_fringe_size}", dump_flag, log_file)

    log("No solution found.", dump_flag, log_file)
    return None, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

def reconstruct_solution(node):
    """
    Reconstruct solution from the goal node

    :param node:
    :return:
    """
    solution = []
    while node.parent:
        solution.append(node.action)
        node = node.parent
    return solution[::-1]


def main():
    if len(sys.argv) < 3:
        print("Usage: expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag>")
        return

    start_file, goal_file = sys.argv[1], sys.argv[2]
    method = sys.argv[3] if len(sys.argv) > 3 else 'a*'
    dump_flag = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else False
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"trace-{timestamp}.txt"

    if dump_flag: # Prepare the header of a log file with the current date and time
        with open(log_file, 'w') as f:
            f.write(f"Command-Line Arguments: [  '{start_file}', '{goal_file}', '{method}', '{sys.argv[4] if len(sys.argv) > 3 else ''}']\n")
            f.write(f"Method Selected: {method}\n")

    start = read_puzzle(start_file)
    goal = read_puzzle(goal_file)

    if VERBOSE:
        print("Start State:")
        for row in start:
            print(row)
        print("Goal State:")
        for row in goal:
            print(row)

    if method.lower() == 'a*':
        solution_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size = a_star(start, goal, dump_flag, log_file)
    elif method.lower() == 'bfs':
        solution_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size = bfs(start, goal, dump_flag, log_file)
    elif method.lower() == 'dfs': # Depth First Search
        solution_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size = dfs(start, goal, dump_flag,
                                                                                            log_file)
    elif method.lower() == 'dfs':  # Uniform CostSearch
        solution_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size = ucs(start, goal, dump_flag,
                                                                                            log_file)
    elif method.lower() == 'dls':  # Depth Limited Search
        solution_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size = dls(start, goal, dump_flag,
                                                                                            log_file)
    elif method.lower() == 'ucs':  #
        solution_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size = ucs(start, goal, dump_flag,
                                                                                            log_file)
    elif method.lower() == 'ids':  # Iterative Deepening Search
        solution_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size = ids(start, goal, dump_flag,
                                                                                            log_file)
    elif method.lower() == 'greedy':  # Greedy Seach
        solution_node, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size = greedy_search(start, goal, dump_flag,
                                                                                            log_file)
    else:
        raise Exception('Search method not implemented')

    if solution_node:
        print(f"Nodes Popped: {nodes_popped}")
        print(f"Nodes Expanded: {nodes_expanded}")
        print(f"Nodes Generated: {nodes_generated}")
        print(f"Max Fringe Size: {max_fringe_size}")
        print(f"Solution Found at depth {solution_node.depth} with cost of {solution_node.cost}.")
        print("Steps:")
        for step in reconstruct_solution(solution_node):
            print(step)
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
