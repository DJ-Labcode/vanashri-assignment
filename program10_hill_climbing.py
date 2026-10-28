"""
Program 10: Hill Climbing                       Domain: Education / EdTech
-----------------------------------------------------------------------------
Problem : Exam timetabling. A school has 8 subjects and 4 exam slots. Students
          enrolled in two subjects cannot sit both exams in the same slot.
          Assign each subject to a slot so that the number of student clashes
          is as small as possible.

State      : slot assigned to each subject, e.g. (0, 2, 1, ...)
Neighbours : change the slot of exactly one subject (8 subjects x 3 other slots = 24)
Objective  : minimise the total clashes (a clash = one student with two exams in one slot)
Method     : Steepest-ascent hill climbing, with random restarts to escape local optima.
"""
import random

SUBJECTS = ["Maths", "Physics", "Chemistry", "Biology", "English", "CS", "Economics", "History"]
SLOTS = 4

enrolments = [
    ["Maths", "Physics", "CS"],
    ["Maths", "Chemistry", "English"],
    ["Physics", "Chemistry", "Biology"],
    ["Biology", "English", "History"],
    ["Economics", "History", "English"],
    ["Maths", "Economics"],
    ["CS", "English"],
    ["Chemistry", "CS", "History"],
    ["Physics", "Economics", "Biology"],
    ["Maths", "Biology", "History"],
]

idx = {s: i for i, s in enumerate(SUBJECTS)}
n = len(SUBJECTS)
shared = [[0] * n for _ in range(n)]          # shared[i][j] = students taking both
for subjects in enrolments:
    for a in subjects:
        for b in subjects:
            if a != b:
                shared[idx[a]][idx[b]] += 1


def clashes(state):
    return sum(shared[i][j] for i in range(n) for j in range(i + 1, n) if state[i] == state[j])


def neighbours(state):
    for i in range(n):
        for slot in range(SLOTS):
            if slot != state[i]:
                yield state[:i] + (slot,) + state[i + 1:]


def hill_climb(state, verbose=False):
    cost, steps = clashes(state), 0
    while True:
        best = min(neighbours(state), key=clashes)
        if clashes(best) >= cost:               # no better neighbour: local optimum
            return state, cost, steps
        state, cost, steps = best, clashes(best), steps + 1
        if verbose:
            print(f"     step {steps}: clashes = {cost}")


def show(state):
    for slot in range(SLOTS):
        subs = [SUBJECTS[i] for i in range(n) if state[i] == slot]
        print(f"   Slot {slot + 1}: {', '.join(subs) if subs else '-'}")


if __name__ == "__main__":
    rng = random.Random(2026)
    print("=== Hill Climbing: Exam Timetable Optimisation ===\n")
    print(f"{n} subjects, {SLOTS} slots, {len(enrolments)} students.\n")

    start = tuple(rng.randrange(SLOTS) for _ in range(n))
    print(f"Run 1 (first attempt) - starting clashes: {clashes(start)}")
    state, cost, steps = hill_climb(start, verbose=True)
    print(f"   Stopped after {steps} steps at clashes = {cost}"
          f"{'  (local optimum, not zero)' if cost > 0 else '  (perfect timetable)'}\n")

    print("Random-restart hill climbing (10 restarts):")
    best_state, best_cost = state, cost
    print(f"   {'Restart':<9}{'Start clashes':<15}{'Final clashes':<15}{'Steps'}")
    for r in range(1, 11):
        s = tuple(rng.randrange(SLOTS) for _ in range(n))
        final, c, st = hill_climb(s)
        print(f"   {r:<9}{clashes(s):<15}{c:<15}{st}")
        if c < best_cost:
            best_state, best_cost = final, c

    print(f"\nBest timetable found (clashes = {best_cost}):")
    show(best_state)