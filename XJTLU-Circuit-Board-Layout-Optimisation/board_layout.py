"""Greedy board allocation reconstructed from report.pdf, appendix pp. 23–26."""
import argparse
import json
from pathlib import Path


def allocate_boards(intersections, limit=0, turns=None):
    """Return 1-based route IDs grouped into feasible boards (not an optimality proof)."""
    n = len(intersections)
    turns = [0] * n if turns is None else turns
    if type(limit) is not int or limit < 0 or len(turns) != n:
        raise ValueError("Require a nonnegative integer limit and one turn count per route.")
    if any(type(t) is not int or not 0 <= t <= limit for t in turns):
        raise ValueError("Each route must fit on a board on its own.")
    if any(len(row) != n for row in intersections):
        raise ValueError("The intersection matrix must be square.")
    if any(type(v) is not int or v < 0 for row in intersections for v in row):
        raise ValueError("Intersection counts must be nonnegative integers.")
    if any(intersections[i][i] != 0 or intersections[i][j] != intersections[j][i]
           for i in range(n) for j in range(n)):
        raise ValueError("The intersection matrix must be symmetric with zero diagonal.")
    remaining = sorted(range(n), key=lambda i: (sum(intersections[i]), i))
    boards = []
    while remaining:
        board = []
        for route in remaining[:]:
            candidate = board + [route]
            if all(turns[i] + sum(intersections[i][j] for j in candidate) <= limit
                   for i in candidate):
                board.append(route)
                remaining.remove(route)
        boards.append([i + 1 for i in sorted(board)])
    return boards


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, nargs="?",
                        default=Path(__file__).parent / "report_cases.json")
    args = parser.parse_args()
    cases = json.loads(args.input.read_text(encoding="utf-8"))
    for name, case in cases.items():
        print(json.dumps({"case": name, "boards": allocate_boards(**case)}, ensure_ascii=False))
