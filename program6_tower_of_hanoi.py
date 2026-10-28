"""
Program 6: Tower of Hanoi
-----------------------------------------------------------------------------
Problem : Move n disks from peg A to peg C using peg B as a helper.
          Rules: move one disk at a time; a larger disk may never be placed on
          a smaller disk.
Education example : Tower of Hanoi is a popular puzzle in maths and
          programming courses because it teaches recursion. Learning apps use
          it to assess a student's planning and problem-solving skills.
Method  : Recursion. T(n) = 2*T(n-1) + 1, so the minimum number of moves is 2^n - 1.
"""

pegs = {}
move_count = 0


def hanoi(n, source, target, helper, verbose=True):
    """Recursively move n disks and update the peg state."""
    global move_count
    if n == 0:
        return
    hanoi(n - 1, source, helper, target, verbose)
    disk = pegs[source].pop()
    pegs[target].append(disk)
    move_count += 1
    if verbose:
        print(f"Move {move_count:2d}: disk {disk} from {source} to {target}"
              f"    A={pegs['A']}  B={pegs['B']}  C={pegs['C']}")
    hanoi(n - 1, helper, target, source, verbose)


def run(n, verbose=True):
    global move_count
    pegs.clear()
    pegs.update({"A": list(range(n, 0, -1)), "B": [], "C": []})
    move_count = 0
    if verbose:
        print(f"Start    : A={pegs['A']}  B={pegs['B']}  C={pegs['C']}")
    hanoi(n, "A", "C", "B", verbose)
    return move_count


if __name__ == "__main__":
    print("=== Tower of Hanoi (Recursion) ===\n")
    print("Solving for 3 disks (disk 1 is the smallest):\n")
    total = run(3)
    print(f"\nTotal moves for 3 disks: {total}  (minimum = 2^3 - 1 = {2**3 - 1})\n")

    print("Minimum number of moves for different numbers of disks:")
    print(f"  {'Disks':<7}{'Moves made':<13}{'2^n - 1'}")
    for n in range(1, 8):
        print(f"  {n:<7}{run(n, verbose=False):<13}{2**n - 1}")