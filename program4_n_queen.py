"""
Program 4: N-Queen Problem (simulation)
-----------------------------------------------------------------------------
Problem : Place N queens on an N x N chessboard so that no two queens attack
          each other (no shared row, column or diagonal).
Education example : Chess is taught in many school/online learning platforms.
          The same constraint model appears in exam-hall seating, where N
          invigilators must be placed so that no two can see each other along
          a row, column or diagonal.
Method  : Backtracking (a constraint-satisfaction search).
"""


def solve_n_queens(n):
    """Return every solution as a list of column positions, one per row."""
    solutions = []
    cols, diag1, diag2 = set(), set(), set()
    placement = []

    def place(row):
        if row == n:
            solutions.append(placement[:])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue                      # square is attacked, skip
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            placement.append(col)
            place(row + 1)
            placement.pop()                   # backtrack
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)

    place(0)
    return solutions


def print_board(solution):
    n = len(solution)
    for row in range(n):
        print("   " + " ".join("Q" if solution[row] == c else "." for c in range(n)))


if __name__ == "__main__":
    print("=== N-Queen Problem (Backtracking) ===\n")

    print("All solutions for N = 4:")
    for i, sol in enumerate(solve_n_queens(4), 1):
        print(f"  Solution {i}: columns per row = {sol}")
        print_board(sol)
        print()

    print("First solution for N = 8:")
    first = solve_n_queens(8)[0]
    print(f"  columns per row = {first}")
    print_board(first)

    print("\nNumber of solutions for different board sizes:")
    print(f"  {'N':<4}{'Solutions'}")
    for n in range(4, 9):
        print(f"  {n:<4}{len(solve_n_queens(n))}")