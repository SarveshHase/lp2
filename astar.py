import copy

class Puzzle:
    def __init__(self, matrix):
        self.matrix = [row[:] for row in matrix]
        self.n = len(matrix)
        self.g_cost = 0  # cost from start to current node

    def __eq__(self, other):
        return self.matrix == other.matrix

    def __hash__(self):
        return hash(str(self.matrix))

    def display_puzzle(self):
        for row in self.matrix:
            print(''.join(str(cell) if cell != 0 else '_' for cell in row))
        print()

    def find_blank(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i][j] == 0:
                    return (i, j)
        return None

    def move_blank(self, dx, dy):
        x, y = self.find_blank()
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.n and 0 <= ny < self.n:
            new_matrix = copy.deepcopy(self.matrix)
            new_matrix[x][y], new_matrix[nx][ny] = new_matrix[nx][ny], new_matrix[x][y]
            new_puzzle = Puzzle(new_matrix)
            new_puzzle.g_cost = self.g_cost + 1
            return new_puzzle
        return None

    def can_move_up(self):
        return self.move_blank(-1, 0)

    def can_move_down(self):
        return self.move_blank(1, 0)

    def can_move_left(self):
        return self.move_blank(0, -1)

    def can_move_right(self):
        return self.move_blank(0, 1)


class AStar:
    def __init__(self, start_state, target_state):
        self.open_list = [start_state]
        self.closed_list = set()
        self.start_state = start_state
        self.target_state = target_state

    def is_goal(self, puzzle):
        return puzzle == self.target_state

    def calculate_manhattan_dist(self, x, curr_pos):
        for i in range(self.target_state.n):
            for j in range(self.target_state.n):
                if self.target_state.matrix[i][j] == x:
                    goal_pos = (i, j)
        return abs(goal_pos[0] - curr_pos[0]) + abs(goal_pos[1] - curr_pos[1])

    def h(self, puzzle):
        dist = 0
        for i in range(puzzle.n):
            for j in range(puzzle.n):
                val = puzzle.matrix[i][j]
                curr_pos = (i, j)
                dist += self.calculate_manhattan_dist(val, curr_pos)
        return dist

    def g(self, puzzle):
        return puzzle.g_cost

    def f(self, puzzle):
        return self.g(puzzle) + self.h(puzzle)
    
    def display_fgh(self, puzzle):
        return f"h={self.h(puzzle)}, g={self.g(puzzle)}, f={self.f(puzzle)}"

    def remove_seen(self, moves):
        return [m for m in moves if m not in self.closed_list]

    def moves_generate(self, puzzle):
        moves = []
        for move_func in [puzzle.can_move_up, puzzle.can_move_down, puzzle.can_move_left, puzzle.can_move_right]:
            new_state = move_func()
            if new_state:
                moves.append(new_state)
        return self.remove_seen(moves)

    def sort_open_list(self):
        self.open_list.sort(key=lambda p: self.f(p))

    def solve(self):
        while self.open_list:
            self.sort_open_list()
            current_state = self.open_list.pop(0)
            print(f"Current State ({self.display_fgh(current_state)})")
            current_state.display_puzzle()

            if self.is_goal(current_state):
                print("Goal reached!")
                return True

            self.closed_list.add(current_state)

            next_moves = self.moves_generate(current_state)
            for move in next_moves:
                if move not in self.open_list:
                    self.open_list.append(move)
                    
        print("Goal not reachable.")
        return False

def main():
    # blank space will be represented internally as 0
    start_matrix = [
        [1, 8, 2],
        [4, 0, 5],
        [7, 3, 6]
    ]
    target_matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    start_puzzle = Puzzle(start_matrix)
    target_puzzle = Puzzle(target_matrix)

    solver = AStar(start_puzzle, target_puzzle)
    solver.solve()

if __name__ == "__main__":
    main()