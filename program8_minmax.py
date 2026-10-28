"""
Program 8: Simulation of a domain-specific game using the Min-Max algorithm
-----------------------------------------------------------------------------
Domain  : Education / EdTech - "Logic Arena", a game module inside a learning
          app. The AI coach plays Tic-Tac-Toe against the student to teach
          strategic thinking (look-ahead, blocking, forcing a win).
Method  : Min-Max search over the full game tree.
          - MAX player (AI coach, 'X')  chooses the move with the highest value.
          - MIN player (student, 'O')   is assumed to choose the lowest value.
          Win = +(1 + empty squares left), Loss = -(1 + empty squares left), Draw = 0,
          so the AI prefers quicker wins and slower losses.
Simulation : (1) one fully shown game, (2) 100 games vs a random student,
          (3) AI vs AI.
"""
import random
from functools import lru_cache

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
AI, STUDENT = "X", "O"


def winner(board):
    for a, b, c in LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


@lru_cache(maxsize=None)
def minimax(board, turn):
    """Value of the position from the AI's point of view (turn = side to move)."""
    w = winner(board)
    empties = board.count(" ")
    if w == AI:
        return 1 + empties
    if w == STUDENT:
        return -(1 + empties)
    if empties == 0:
        return 0
    values = []
    for i in range(9):
        if board[i] == " ":
            child = board[:i] + turn + board[i + 1:]
            values.append(minimax(child, STUDENT if turn == AI else AI))
    return max(values) if turn == AI else min(values)


def best_move(board, turn):
    """Pick the move with the best Min-Max value for the side to move."""
    scored = []
    for i in range(9):
        if board[i] == " ":
            child = board[:i] + turn + board[i + 1:]
            scored.append((minimax(child, STUDENT if turn == AI else AI), i))
    if turn == AI:
        return max(scored, key=lambda s: (s[0], -s[1]))[1]
    return min(scored, key=lambda s: (s[0], s[1]))[1]


def student_move(board, rng):
    return rng.choice([i for i in range(9) if board[i] == " "])


def show(board):
    rows = [f" {board[r]} | {board[r + 1]} | {board[r + 2]}" for r in (0, 3, 6)]
    print("\n   ---+---+---\n".join("  " + r for r in rows))


def play(x_player, o_player, rng, verbose=False):
    """x_player / o_player are 'ai' or 'student'. X moves first."""
    board, turn = " " * 9, "X"
    while winner(board) is None and " " in board:
        who = x_player if turn == "X" else o_player
        if who == "ai":
            # the AI always evaluates from its own side
            global AI, STUDENT
            AI, STUDENT = turn, ("O" if turn == "X" else "X")
            minimax.cache_clear()
            move = best_move(board, turn)
        else:
            move = student_move(board, rng)
        board = board[:move] + turn + board[move + 1:]
        if verbose:
            print(f"\n{turn} ({who}) plays square {move + 1}:")
            show(board)
        turn = "O" if turn == "X" else "X"
    return winner(board)


if __name__ == "__main__":
    rng = random.Random(7)
    print("=== Logic Arena: Tic-Tac-Toe with Min-Max AI coach ===")
    print("Squares are numbered 1-9 from the top-left corner.\n")

    print("--- Game 1: AI coach (X) vs random student (O) ---")
    result = play("ai", "student", rng, verbose=True)
    print("\nResult:", f"{result} wins" if result else "Draw")

    print("\n--- Simulation of 100 games each ---")
    for label, xp, op in [("AI (X) vs random student (O)", "ai", "student"),
                          ("random student (X) vs AI (O)", "student", "ai"),
                          ("AI (X) vs AI (O)",             "ai", "ai")]:
        tally = {"X": 0, "O": 0, None: 0}
        for _ in range(100):
            tally[play(xp, op, rng)] += 1
        print(f"{label:<32} X wins: {tally['X']:3d}   O wins: {tally['O']:3d}"
              f"   Draws: {tally[None]:3d}")