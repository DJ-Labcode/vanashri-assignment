"""
Program 2: Breadth First Search (BFS)          Domain: Education / EdTech
--------------------------------------------------------------------------
Scenario : Same course prerequisite graph as Program 1.
Use of BFS:
  (a) Level-order traversal  -> courses grouped into a semester-wise plan.
  (b) Shortest learning path -> fewest courses needed to reach a target course.
"""
from collections import deque

course_graph = {
    "Programming Basics": ["Data Structures", "Discrete Maths", "Databases"],
    "Data Structures":    ["Algorithms", "Operating Systems"],
    "Discrete Maths":     ["Algorithms", "Probability"],
    "Databases":          ["Data Mining"],
    "Algorithms":         ["Machine Learning"],
    "Operating Systems":  [],
    "Probability":        ["Machine Learning", "Data Mining"],
    "Data Mining":        ["Machine Learning"],
    "Machine Learning":   ["Deep Learning", "AI in Education"],
    "Deep Learning":      ["AI in Education"],
    "AI in Education":    [],
}


def bfs_levels(graph, start):
    """Return {course: level} where level = fewest steps from the start course."""
    level = {start: 0}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            if nxt not in level:
                level[nxt] = level[node] + 1
                queue.append(nxt)
    return order, level


def bfs_shortest_path(graph, start, goal):
    """BFS with a parent map; the first time the goal is reached is the shortest path."""
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]
        for nxt in graph[node]:
            if nxt not in parent:
                parent[nxt] = node
                queue.append(nxt)
    return None


if __name__ == "__main__":
    start, goal = "Programming Basics", "AI in Education"

    print("=== BFS on the Course Prerequisite Graph ===\n")
    order, level = bfs_levels(course_graph, start)
    print("(a) BFS visiting order:")
    for i, course in enumerate(order, 1):
        print(f"   {i:2d}. {course}")

    print("\n    Semester-wise plan (BFS levels):")
    for lv in range(max(level.values()) + 1):
        courses = [c for c in order if level[c] == lv]
        print(f"      Semester {lv + 1}: {', '.join(courses)}")

    print(f"\n(b) Shortest learning path: {start} -> {goal}")
    path = bfs_shortest_path(course_graph, start, goal)
    print("   " + " -> ".join(path))
    print(f"   Minimum number of courses to complete: {len(path)}")