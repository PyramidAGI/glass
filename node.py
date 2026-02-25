from typing import Tuple
from pojar import POJAR
from node_types import PlanningType, ControllingType, CausalType


class Node:
    """A processing node on the chessboard landscape.

    Valid positions satisfy (row + col) % 2 == 0.
    """

    def __init__(
        self,
        row: int,
        col: int,
        planning_type: PlanningType,
        controlling_type: ControllingType,
        causal_type: CausalType,
        pojar: POJAR = None,
        json1: dict = None,
    ):
        if (row + col) % 2 != 0:
            raise ValueError(f"Position ({row}, {col}) is not a valid chessboard node position.")
        self.row = row
        self.col = col
        self.planning_type = planning_type
        self.controlling_type = controlling_type
        self.causal_type = causal_type
        self.pojar = pojar or POJAR()
        self.json1: dict = json1 or {}
        self.json2: dict = {}

    @property
    def position(self) -> Tuple[int, int]:
        return (self.row, self.col)

    @property
    def label(self) -> str:
        return f"Node({self.row},{self.col})[{self.planning_type.value}/{self.controlling_type.value}/{self.causal_type.value}]"

    def execute(self) -> None:
        """Run POJAR algo (if enabled) then both loops."""
        if not self.pojar.run:
            return
        self.json2 = self.pojar.algo(self.json1)

    def loop1(self) -> dict:
        """Loop1: Belief → Measure.

        The node treats its json1 as its current belief and produces a
        measurement (json2) by running the algo.  Returns the measurement.
        """
        belief = dict(self.json1)
        measure = self.pojar.algo(belief)
        self.json2 = measure
        return measure

    def loop2(self, neighbours: list) -> dict:
        """Loop2: Influence → Measure.

        The node broadcasts its current json2 as an influence signal to each
        neighbour (setting their json1), then re-measures its own state.
        Returns the updated json2.
        """
        influence = dict(self.json2)
        for neighbour in neighbours:
            neighbour.json1.update(influence)
        measure = self.pojar.algo(self.json1)
        self.json2 = measure
        return measure

    def __repr__(self) -> str:
        return self.label
