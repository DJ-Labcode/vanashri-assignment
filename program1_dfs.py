"""
Program 1: Depth First Search (DFS)            Domain: Education / EdTech
--------------------------------------------------------------------------
Scenario : An online learning platform stores its course catalogue as a
           prerequisite graph (course -> courses it unlocks).
Use of DFS:
  (a) Explore the catalogue starting from a beginner course.
  (b) Find one learning path from a beginner course to a target course.
  (c) Count every possible learning path to the target (full DFS with backtracking).
"""

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


def dfs_recursive(graph, node, visited=None, order=None):
    """Recursive DFS: returns the order in which courses are explored."""
    if visited is None:
        visited, order = set(), []
    visited.add(node)
    order.append(node)
    for nxt in graph[node]:
        if nxt not in visited:
            dfs_recursive(graph, nxt, visited, order)
    return order


def dfs_path(graph, start, goal):
    """Iterative DFS using an explicit stack; returns the first path found."""
    stack = [(start, [start])]
    visited = set()
    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)
        # reversed() so that the first listed course is explored first
        for nxt in reversed(graph[node]):
            if nxt not in visited:
                stack.append((nxt, path + [nxt]))
    return None


def dfs_all_paths(graph, node, goal, path=None, result=None):
    """DFS with backtracking: collects every simple path from node to goal."""
    if path is None:
        path, result = [], []
    path.append(node)
    if node == goal:
        result.append(list(path))
    else:
        for nxt in graph[node]:
            if nxt not in path:
                dfs_all_paths(graph, nxt, goal, path, result)
    path.pop()                       # backtrack
    return result


if __name__ == "__main__":
    start, goal = "Programming Basics", "Machine Learning"

    print("=== DFS on the Course Prerequisite Graph ===\n")
    print("(a) DFS exploration order from", repr(start))
    for i, course in enumerate(dfs_recursive(course_graph, start), 1):
        print(f"   {i:2d}. {course}")

    print(f"\n(b) First learning path found by DFS: {start} -> {goal}")
    path = dfs_path(course_graph, start, goal)
    print("   " + " -> ".join(path))
    print(f"   Number of courses on this path: {len(path)}")

    print(f"\n(c) All learning paths from {start!r} to {goal!r}")
    paths = dfs_all_paths(course_graph, start, goal)
    for i, p in enumerate(paths, 1):
        print(f"   Path {i}: " + " -> ".join(p))
    print(f"   Total paths: {len(paths)}")