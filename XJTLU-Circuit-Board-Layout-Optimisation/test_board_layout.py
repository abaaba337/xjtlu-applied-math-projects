import json
from pathlib import Path
import unittest

from board_layout import allocate_boards


class BoardRegression(unittest.TestCase):
    def test_report_cases_and_constraints(self):
        cases = json.loads((Path(__file__).parent / "report_cases.json").read_text())
        for case, expected in zip(cases.values(), (3, 2, 3)):
            boards = allocate_boards(**case)
            self.assertEqual(len(boards), expected)
            matrix = case["intersections"]
            self.assertEqual(sorted(i for board in boards for i in board), list(range(1, 11)))
            for board in boards:
                for route in board:
                    used = case.get("turns", [0] * 10)[route - 1]
                    used += sum(matrix[route - 1][other - 1] for other in board)
                    self.assertLessEqual(used, case["limit"])

    def test_rejects_infeasible_and_asymmetric_input(self):
        for matrix, turns in [([[0]], [1]), ([[0, 1], [0, 0]], [0, 0])]:
            with self.assertRaises(ValueError):
                allocate_boards(matrix, turns=turns)


if __name__ == "__main__":
    unittest.main()
