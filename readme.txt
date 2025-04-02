Task is to build an agent to solve a modifed version of the 8 puzzle problem (called the Expense 8 puzzle problem). The task is still to take a 3X3 grid on which 8 tiles have been placed, where you can only move one tile at a time to an adjacent location (as long as it is blank) and figure out the order in which to move the tiles to get it to a desired configuration. However now the number on the tile now also represents the cot of moving that tile (moving the tile marked 6 costs 6).
Your program should be called expense_8_puzzle and the command line invocation should follow the following format:
expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag>
<start-file> and <goal-file> are required.
<method> can be
bfs - Breadth First Search ucs - Uniform CostSearch
dfs - Depth First Search
dls - Depth Limited Search (Note: Depth Limit will be obtained as a Console Input)
ids - Iterative Deepening Search
greedy - Greedy Seach
a* - A* Search (Note: if no <method> is given, this should be the default option)
If <dump-flag> is given as true, search trace is dumped for analysis in trace-<date>-<time>.txt (Note: if <dump-flag> is not given, assume it is false) search trace contains: fringe and closed set contents per loop of search(and per iteration for IDS), counts of nodes expanded and nodes
Both start file and goal file need to follow the format as shown here:


How to Run the Code:

Navigate to the directory where the code file is downloaded
Use the command prompt to run the code. 
Input files(start.txt goal.txt) should be placed in the folder

command:
	python expense_8_puzzle.py start.txt goal.txt <method> true

	python expense_8_puzzle.py start.txt goal.txt bfs true
	python expense_8_puzzle.py start.txt goal.txt dfs true
	python expense_8_puzzle.py start.txt goal.txt ucs true
	python expense_8_puzzle.py start.txt goal.txt ids true
	python expense_8_puzzle.py start.txt goal.txt a* true
	python expense_8_puzzle.py start.txt goal.txt greedy true
	python expense_8_puzzle.py start.txt goal.txt dls true  
		with depth limit : 12 
	
- If the true flag enables logging and search trace is dumped in treacefile.txt. Else, logging is disabled.


Code Structure:

The expense_8_puzzle.py is a Python script to solve the 8-puzzle problem using various search algorithms.

Prgoram imports modules sys for handling command-line arguments, datetime for generating timestamps, deque from the collections module for implementing queues.

A global variable named VERBOSE is defined to control verbose output during debugging.

Function called read_puzzle used to read the puzzle configuration from a file.

The heuristic function (heuristic) estimates the cost from the current state to the goal state.

Implemented Searches:

Breadth-First Search (bfs): BFS explores the search tree level by level, using a queue (deque) to maintain the order of nodes to be expanded. It guarantees finding the shallowest solution but can be memory-intensive for large search spaces.

Depth-First Search (dfs): DFS explores as deep as possible along each branch before backtracking. It uses a stack (implemented as a list) to manage the nodes to be expanded. While DFS can be more memory-efficient than BFS, it is not guaranteed to find the shortest path to the goal and can get stuck in deep or infinite branches.

A* Search : This algorithm uses both the actual cost from the start node (g(n)) and the heuristic estimate to the goal (h(n)) to prioritize nodes. It maintains an open list (a priority queue) and a closed set to keep track of explored states. At each step, it selects the node with the lowest total estimated cost (f(n) = g(n) + h(n)), expands it by generating its successors using get_successors, and continues this process until it reaches the goal state.

Uniform Cost Search (ucs): UCS is similar to A* but does not use a heuristic. It prioritizes nodes based solely on the cumulative cost to reach them (g(n)). This algorithm is optimal and complete but can be less efficient than A* in terms of time and space.

Depth-Limited Search (dls): DLS is a variation of DFS that limits how deep the search can go. The depth limit is specified by the user. This method prevents the search from going down infinite paths but requires knowledge of a reasonable depth limit to be effective.

Iterative Deepening Search (ids): IDS combines the benefits of BFS and DFS by performing DLS repeatedly with increasing depth limits. It starts with a depth limit of zero and increments the limit until a solution is fouond. This method is both complete and optimal like BFS but uses less memory. The IDS function uses a helper function dls_with_limit to perform depth-limited searches at each iteration.

Greedy Search (greedy): This algorithm uses the heuristic function heuristic to select the next node to expand, prioritizing nodes that appear closest to the goal according to the heuristic. It does not consider the cost to reach a node (g(n)) and can be faster but may not find the optimal solution.

Each of these algorithms maintains performance metrics: the number of nodes popped from the open list, the number of nodes expanded, the number of nodes generated, and the maximum size of the fringe (open list). These metrics provide insight into the efficiency of each algorithm for a given problem.

To rceonstruct the solution path once the goal is found, the program includes a function called reconstruct_solution that backtracks from the goal node to the start node using the parent references in each Node. It collects the actions taken at each step, reversing the list to present the sequence from start to goal.

The main functoin serves as the entry point of the program. It begins by parsing command-line arguments to determine the start file, goal file, chosen search method, and whether logging is enabled.



