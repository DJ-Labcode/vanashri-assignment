"""
Program 9: Alpha-Beta Pruning                  Domain: Education / EdTech
-----------------------------------------------------------------------------
Part A - Adaptive learning tree
  An AI tutor must decide which topic to teach next.
    Level 0 (MAX): tutor chooses a topic.
    Level 1 (MIN): the student's worst-case reaction to that topic.
    Level 2 (MAX): tutor chooses the question difficulty (Easy / Medium / Hard).
    Leaves       : expected learning gain (0-10).
  Alpha-Beta gives the same decision as Min-Max but skips branches that cannot
  change the result.

Part B - Same Tic-Tac-Toe "Logic Arena" game as Program 8
  Compares how many positions Min-Max and Alpha-Beta must examine.
"""
import math

# ----------------------------- Part A ------------------------------------
TOPICS     = ["Algebra", "Geometry", "Statistics"]
REACTIONS  = ["Struggles", "Average", "Confident"]
DIFFICULTY = ["Easy", "Medium", "Hard"]

# tree[topic][reaction][difficulty] = learning gain
tree = [
    [[3, 5, 6], [9, 1, 2], [0, 7, 4]],
    [[2, 1, 3], [5, 0, 4], [8, 2, 6]],
    [[7, 2, 5], [4, 8, 3], [6, 9, 1]],
]

leaf_count = 0


def minimax_tree(node, depth, is_max):
    global leaf_count
    if depth == 3:
        leaf_count += 1
        return node
    vals = [minimax_tree(c, depth + 1, not is_max) for c in node]
    return max(vals) if is_max else min(vals)


def alphabeta_tree(node, depth, is_max, alpha, beta, path, trace):
    global leaf_count
    if depth == 3:
        leaf_count += 1
        return node
    best = -math.inf if is_max else math.inf
    for k, child in enumerate(node):
        label = [TOPICS, REACTIONS, DIFFICULTY][depth][k]
        val = alphabeta_tree(child, depth + 1, not is_max, alpha, beta, path + [label], trace)
        if is_max:
            best = max(best, val)
            alpha = max(alpha, best)
        else:
            best = min(best, val)
            beta = min(beta, best)
        if alpha >= beta:
            skipped = len(node) - k - 1
            if skipped:
                where = " > ".join(path) or "root"
                trace.append(f"   PRUNE under {where} after '{label}': "
                             f"alpha={alpha}, beta={beta}, {skipped} sibling(s) skipped")
            break
    return best


# ----------------------------- Part B ------------------------------------
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
nodes = 0


def winner(b):
    for x, y, z in LINES:
        if b[x] != " " and b[x] == b[y] == b[z]:
            return b[x]
    return None


def mm(b, turn):
    global nodes
    nodes += 1
    w = winner(b)
    if w:
        return 1 if w == "X" else -1
    if " " not in b:
        return 0
    vals = [mm(b[:i] + turn + b[i + 1:], "O" if turn == "X" else "X")
            for i in range(9) if b[i] == " "]
    return max(vals) if turn == "X" else min(vals)


def ab(b, turn, alpha, beta):
    global nodes
    nodes += 1
    w = winner(b)
    if w:
        return 1 if w == "X" else -1
    if " " not in b:
        return 0
    if turn == "X":
        best = -math.inf
        for i in range(9):
            if b[i] == " ":
                best = max(best, ab(b[:i] + "X" + b[i + 1:], "O", alpha, beta))
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
        return best
    best = math.inf
    for i in range(9):
        if b[i] == " ":
            best = min(best, ab(b[:i] + "O" + b[i + 1:], "X", alpha, beta))
            beta = min(beta, best)
            if alpha >= beta:
                break
    return best


if __name__ == "__main__":
    print("=== Alpha-Beta Pruning ===\n")
    print("Part A: Adaptive learning tree (27 leaf nodes)\n")

    leaf_count = 0
    mm_value = minimax_tree(tree, 0, True)
    mm_leaves = leaf_count

    leaf_count = 0
    trace = []
    ab_value = alphabeta_tree(tree, 0, True, -math.inf, math.inf, [], trace)
    ab_leaves = leaf_count

    for line in trace:
        print(line)
    best_topic = max(range(3), key=lambda t: minimax_tree(tree[t], 1, False))
    print(f"\nMin-Max value     : {mm_value}   (leaves evaluated: {mm_leaves})")
    print(f"Alpha-Beta value  : {ab_value}   (leaves evaluated: {ab_leaves})")
    print(f"Leaves skipped    : {mm_leaves - ab_leaves} of {mm_leaves}")
    print(f"Tutor's decision  : teach '{TOPICS[best_topic]}' next "
          f"(guaranteed learning gain >= {ab_value})")

    print("\nPart B: Tic-Tac-Toe game tree from the empty board\n")
    empty = " " * 9
    nodes = 0
    v1 = mm(empty, "X")
    n1 = nodes
    nodes = 0
    v2 = ab(empty, "X", -math.inf, math.inf)
    n2 = nodes
    print(f"  {'Algorithm':<12}{'Game value':<12}{'Positions examined'}")
    print(f"  {'Min-Max':<12}{v1:<12}{n1:,}")
    print(f"  {'Alpha-Beta':<12}{v2:<12}{n2:,}")
    print(f"\n  Alpha-Beta examined {100 * (1 - n2 / n1):.1f}% fewer positions and")
    print("  returned the same value (0 = draw with best play).")