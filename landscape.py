"""NodeLandscape: staggered chessboard grid of nodes.

Valid positions satisfy (row + col) % 2 == 0, mirroring the black squares
of a chessboard when the top-left corner is black.
"""

from typing import Dict, List, Optional, Tuple
from loops import run_loop1, run_loop2


class NodeLandscape:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        # Map from (row, col) → Node
        self._grid: Dict[Tuple[int, int], object] = {}

    # ------------------------------------------------------------------
    # Grid management
    # ------------------------------------------------------------------

    @staticmethod
    def is_valid_position(row: int, col: int) -> bool:
        return (row + col) % 2 == 0

    def add_node(self, node) -> None:
        pos = (node.row, node.col)
        if not self.is_valid_position(*pos):
            raise ValueError(f"Position {pos} is not a valid chessboard position.")
        if not (0 <= node.row < self.rows and 0 <= node.col < self.cols):
            raise ValueError(f"Position {pos} is outside the grid ({self.rows}×{self.cols}).")
        self._grid[pos] = node

    def get_node(self, row: int, col: int) -> Optional[object]:
        return self._grid.get((row, col))

    def all_nodes(self) -> List[object]:
        return list(self._grid.values())

    def get_neighbours(self, node) -> List[object]:
        """Return the (up to 4) diagonally adjacent nodes that exist in the grid."""
        r, c = node.row, node.col
        neighbours = []
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighbour = self._grid.get((r + dr, c + dc))
            if neighbour is not None:
                neighbours.append(neighbour)
        return neighbours

    # ------------------------------------------------------------------
    # Information flow
    # ------------------------------------------------------------------

    def propagate_down(self) -> None:
        """Pass json2 of each node into json1 of its lower-row neighbours."""
        for (row, col), node in sorted(self._grid.items()):
            for dr, dc in [(1, -1), (1, 1)]:
                child = self._grid.get((row + dr, col + dc))
                if child is not None:
                    child.json1.update(node.json2)

    def propagate_up(self) -> None:
        """Pass json2 of each node into json1 of its upper-row neighbours."""
        for (row, col), node in sorted(self._grid.items(), reverse=True):
            for dr, dc in [(-1, -1), (-1, 1)]:
                parent = self._grid.get((row + dr, col + dc))
                if parent is not None:
                    parent.json1.update(node.json2)

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Full execution cycle:
        1. propagate_down  (context flows from top to bottom)
        2. execute + Loop1 on every node (row-major order)
        3. Loop2 on every node (influence exchange with neighbours)
        4. propagate_up    (measurements flow from bottom to top)
        """
        self.propagate_down()

        nodes_by_row = sorted(self._grid.values(), key=lambda n: (n.row, n.col))
        for node in nodes_by_row:
            node.execute()
            run_loop1(node)

        for node in nodes_by_row:
            run_loop2(node, self.get_neighbours(node))

        self.propagate_up()

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def display(self) -> str:
        lines = []
        for row in range(self.rows):
            cells = []
            for col in range(self.cols):
                node = self._grid.get((row, col))
                if node is not None:
                    cells.append(f"[{node.planning_type.value[0].upper()}"
                                 f"{node.controlling_type.value[0].upper()}"
                                 f"{node.causal_type.value[0].upper()}]")
                elif self.is_valid_position(row, col):
                    cells.append("[   ]")
                else:
                    cells.append("     ")
            lines.append(" ".join(cells))
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"NodeLandscape({self.rows}×{self.cols}, {len(self._grid)} nodes)"
