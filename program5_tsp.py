"""
Program 5: Travelling Salesman Problem using AI techniques
-----------------------------------------------------------------------------
Scenario : A campus shuttle (or a visiting tutor) must start at the Admin
           Block, visit every other campus location exactly once and return.
           Find the shortest tour.

AI techniques used
  1. Nearest-Neighbour heuristic   (greedy constructive search)
  2. 2-opt local search            (hill-climbing improvement of a tour)
  3. Simulated Annealing           (stochastic search that can escape local optima)
  4. Brute force                   (exact answer, used only to check the AI results)
"""
import math
import random
from itertools import permutations

places = {
    "Admin Block":     (2, 3),
    "Library":         (8, 9),
    "Science Lab":     (14, 4),
    "Hostel":          (19, 12),
    "Sports Complex":  (6, 16),
    "Canteen":         (12, 15),
    "Auditorium":      (17, 2),
    "Computer Centre": (4, 10),
}
names = list(places)
N = len(names)


def dist(a, b):
    (x1, y1), (x2, y2) = places[names[a]], places[names[b]]
    return math.hypot(x1 - x2, y1 - y2)


D = [[dist(i, j) for j in range(N)] for i in range(N)]


def tour_length(tour):
    return sum(D[tour[i]][tour[(i + 1) % N]] for i in range(N))


def nearest_neighbour(start=0):
    tour, left = [start], set(range(N)) - {start}
    while left:
        nxt = min(left, key=lambda c: D[tour[-1]][c])
        tour.append(nxt)
        left.remove(nxt)
    return tour


def two_opt(tour):
    best = tour[:]
    improved = True
    while improved:
        improved = False
        for i in range(1, N - 1):
            for j in range(i + 1, N):
                cand = best[:i] + best[i:j + 1][::-1] + best[j + 1:]
                if tour_length(cand) < tour_length(best) - 1e-9:
                    best, improved = cand, True
    return best


def simulated_annealing(start_tour, temp=50.0, cooling=0.995, min_temp=0.01, seed=42):
    rng = random.Random(seed)
    cur, cur_len = start_tour[:], tour_length(start_tour)
    best, best_len = cur[:], cur_len
    while temp > min_temp:
        i, j = sorted(rng.sample(range(1, N), 2))
        cand = cur[:i] + cur[i:j + 1][::-1] + cur[j + 1:]
        delta = tour_length(cand) - cur_len
        if delta < 0 or rng.random() < math.exp(-delta / temp):
            cur, cur_len = cand, cur_len + delta
            if cur_len < best_len:
                best, best_len = cur[:], cur_len
        temp *= cooling
    return best


def brute_force():
    best, best_len = None, float("inf")
    for perm in permutations(range(1, N)):
        tour = [0] + list(perm)
        length = tour_length(tour)
        if length < best_len:
            best, best_len = tour, length
    return best


def show(title, tour):
    stops = [names[i] for i in tour] + [names[tour[0]]]
    print(title)
    print("   Route   : " + stops[0])
    for stop in stops[1:]:
        print("             -> " + stop)
    print(f"   Distance: {tour_length(tour):.2f} units\n")


if __name__ == "__main__":
    print("=== Travelling Salesman Problem: Campus Shuttle Route ===\n")
    print(f"Locations: {N}   (start/end: {names[0]})\n")

    nn = nearest_neighbour()
    show("1. Nearest-Neighbour heuristic", nn)

    opt2 = two_opt(nn)
    show("2. Nearest-Neighbour + 2-opt local search", opt2)

    sa = simulated_annealing(nn)
    show("3. Simulated Annealing (seed 42)", sa)

    opt = brute_force()
    show("4. Brute force (exact optimum, 7! = 5040 tours)", opt)

    print("Comparison with the exact optimum:")
    best = tour_length(opt)
    for label, t in [("Nearest-Neighbour", nn), ("2-opt", opt2), ("Simulated Annealing", sa)]:
        gap = (tour_length(t) - best) / best * 100
        print(f"   {label:<22}{tour_length(t):8.2f}   ({gap:5.2f}% above optimum)")