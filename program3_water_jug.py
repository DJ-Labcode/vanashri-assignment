"""
Program 3: Water Jug Problem
-----------------------------------------------------------------------------
Classic problem : You have a 4-litre jug and a 3-litre jug (no markings) and an
                  unlimited water supply. Measure exactly 2 litres in the 4-litre jug.

Similar problem (Education / EdTech version) - "Chemistry Lab Beaker Challenge":
    A school chemistry lab has two unmarked beakers of capacity 5 mL and 3 mL and
    an unlimited supply of distilled water plus a drain. A student must measure
    exactly 4 mL of water in the 5 mL beaker for an experiment. The allowed
    operations are: fill a beaker, empty a beaker, or pour from one beaker into
    the other until the source is empty or the destination is full.
    The same state-space model works for both problems.

State  : (x, y) = water in jug 1 and jug 2.
Search : Breadth First Search guarantees the minimum number of steps.
"""
from collections import deque
from math import gcd


def successors(state, cap1, cap2):
    x, y = state
    pour_1_to_2 = min(x, cap2 - y)
    pour_2_to_1 = min(y, cap1 - x)
    return [
        ("Fill jug 1",        (cap1, y)),
        ("Fill jug 2",        (x, cap2)),
        ("Empty jug 1",       (0, y)),
        ("Empty jug 2",       (x, 0)),
        ("Pour jug 1 -> 2",   (x - pour_1_to_2, y + pour_1_to_2)),
        ("Pour jug 2 -> 1",   (x + pour_2_to_1, y - pour_2_to_1)),
    ]


def solve(cap1, cap2, target):
    # Quick feasibility test: target must be a multiple of gcd and fit in a jug.
    if target > max(cap1, cap2) or target % gcd(cap1, cap2) != 0:
        return None
    start = (0, 0)
    parent = {start: None}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        if target in state:
            steps = []
            while parent[state] is not None:
                action, prev = parent[state]
                steps.append((action, state))
                state = prev
            return steps[::-1]
        for action, nxt in successors(state, cap1, cap2):
            if nxt not in parent:
                parent[nxt] = (action, state)
                queue.append(nxt)
    return None


def show(cap1, cap2, target, title):
    print(f"--- {title}: jugs {cap1} and {cap2}, target {target} ---")
    steps = solve(cap1, cap2, target)
    if steps is None:
        print(f"No solution: {target} is not reachable "
              f"(gcd({cap1},{cap2}) = {gcd(cap1, cap2)}).\n")
        return
    print(f"{'Step':<5}{'Action':<20}{'State (jug1, jug2)'}")
    print(f"{0:<5}{'Start':<20}(0, 0)")
    for i, (action, state) in enumerate(steps, 1):
        print(f"{i:<5}{action:<20}{state}")
    print(f"Solved in {len(steps)} steps.\n")


if __name__ == "__main__":
    print("=== Water Jug Problem (BFS state-space search) ===\n")
    show(4, 3, 2, "Classic problem")
    show(5, 3, 4, "Chemistry Lab Beaker Challenge (EdTech version)")
    show(6, 4, 5, "Unsolvable check")