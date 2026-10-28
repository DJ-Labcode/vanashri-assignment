"""
Program 7: Blocks World Problem
-----------------------------------------------------------------------------
Problem : A robot arm can move one clear block (nothing on top of it) at a
          time, either onto the table or onto another clear block. Transform the
          initial arrangement of blocks into the goal arrangement using the
          fewest moves.
Education example : Blocks World is used in AI courses and in robotics
          classrooms (educational robot arms) to teach planning.
Representation : a state is a set of stacks; each stack is listed bottom -> top.
Method  : Breadth First Search over the state space (finds the shortest plan).
"""
from collections import deque


def normalise(stacks):
    """Order of stacks on the table does not matter, so sort them."""
    return tuple(sorted(tuple(s) for s in stacks if s))


def successors(state):
    """Yield (description, new_state) for every legal move."""
    stacks = [list(s) for s in state]
    for i, src in enumerate(stacks):
        block = src[-1]                                   # only the top block is clear
        # 1) move onto another stack
        for j, dst in enumerate(stacks):
            if i == j:
                continue
            new = [list(s) for s in stacks]
            new[i].pop()
            new[j].append(block)
            below = src[-2] if len(src) > 1 else "table"
            yield f"Move {block} from {below} onto {dst[-1]}", normalise(new)
        # 2) move onto the table (only useful if it is not already alone)
        if len(src) > 1:
            new = [list(s) for s in stacks]
            new[i].pop()
            new.append([block])
            yield f"Move {block} from {src[-2]} onto table", normalise(new)


def solve(initial, goal):
    start, target = normalise(initial), normalise(goal)
    parent = {start: None}
    queue = deque([start])
    explored = 0
    while queue:
        state = queue.popleft()
        explored += 1
        if state == target:
            plan = []
            while parent[state] is not None:
                action, prev = parent[state]
                plan.append((action, state))
                state = prev
            return plan[::-1], explored
        for action, nxt in successors(state):
            if nxt not in parent:
                parent[nxt] = (action, state)
                queue.append(nxt)
    return None, explored


def draw(state):
    height = max(len(s) for s in state)
    for level in range(height - 1, -1, -1):
        print("      " + "   ".join(s[level] if level < len(s) else " " for s in state))
    print("      " + "   ".join("-" for _ in state) + "   (table)")


if __name__ == "__main__":
    # bottom -> top
    initial = [["A", "B"], ["C", "D"]]          # B on A, D on C
    goal    = [["D", "C", "B", "A"]]            # one tower: D at bottom, A on top

    print("=== Blocks World (BFS planning) ===\n")
    print("Initial state:")
    draw(normalise(initial))
    print("\nGoal state:")
    draw(normalise(goal))

    plan, explored = solve(initial, goal)
    print(f"\nShortest plan found: {len(plan)} moves  (states explored: {explored})\n")
    for i, (action, state) in enumerate(plan, 1):
        print(f"Step {i}: {action}")
        draw(state)
        print()