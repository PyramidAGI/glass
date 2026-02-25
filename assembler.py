"""GoalAssembler: translates a goal JSON into a populated NodeLandscape."""

from typing import Dict, List
from node import Node
from node_types import PlanningType, ControllingType, CausalType
from pojar import POJAR
from landscape import NodeLandscape

# Map string names (from goal JSON) to enum values
_PLANNING_MAP: Dict[str, PlanningType] = {t.value: t for t in PlanningType}
_CONTROLLING_MAP: Dict[str, ControllingType] = {t.value: t for t in ControllingType}
_CAUSAL_MAP: Dict[str, CausalType] = {t.value: t for t in CausalType}

# Default node type combination when not specified
_DEFAULT_PLANNING = PlanningType.NAVIGATOR
_DEFAULT_CONTROLLING = ControllingType.CONTROLLER
_DEFAULT_CAUSAL = CausalType.CAUSAL


def _build_algo(algo_spec: dict):
    """Return a callable algo from a spec dict.

    Supported specs:
      { "type": "passthrough" }           — returns json1 unchanged
      { "type": "merge", "data": {...} }  — merges extra data into json1
      { "type": "inline", "code": "..." } — executes a Python lambda string
    """
    spec_type = algo_spec.get("type", "passthrough")

    if spec_type == "passthrough":
        return lambda j: dict(j)

    if spec_type == "merge":
        extra = algo_spec.get("data", {})
        return lambda j, _e=extra: {**j, **_e}

    if spec_type == "inline":
        code = algo_spec.get("code", "lambda j: j")
        fn = eval(code)  # noqa: S307  (user-supplied trusted code)
        return fn

    return lambda j: dict(j)


class GoalAssembler:
    """Assembles a NodeLandscape from a goal specification dict.

    Goal schema:
    {
        "goal": "description string",
        "grid_size": [rows, cols],
        "required_node_types": [
            {
                "planning": "navigator",
                "controlling": "controller",
                "causal": "causal",
                "algo": { "type": "passthrough" },
                "problem_story": {},
                "onto": [],
                "json_target": {}
            }
        ],
        "constraints": {}
    }

    Nodes are placed on valid chessboard positions in row-major order.
    If more node type specs are provided than available positions, extras
    are ignored.  If fewer are provided, remaining positions use the default
    Navigator/Controller/Causal type.
    """

    def assemble(self, goal: dict) -> NodeLandscape:
        rows, cols = goal.get("grid_size", [4, 4])
        landscape = NodeLandscape(rows, cols)

        node_specs: List[dict] = goal.get("required_node_types", [])

        # Collect valid positions in row-major order
        valid_positions = [
            (r, c)
            for r in range(rows)
            for c in range(cols)
            if NodeLandscape.is_valid_position(r, c)
        ]

        for idx, pos in enumerate(valid_positions):
            spec = node_specs[idx] if idx < len(node_specs) else {}

            planning = _PLANNING_MAP.get(spec.get("planning", ""), _DEFAULT_PLANNING)
            controlling = _CONTROLLING_MAP.get(spec.get("controlling", ""), _DEFAULT_CONTROLLING)
            causal = _CAUSAL_MAP.get(spec.get("causal", ""), _DEFAULT_CAUSAL)

            algo = _build_algo(spec.get("algo", {"type": "passthrough"}))
            pojar = POJAR(
                problem_story=spec.get("problem_story", {}),
                onto=spec.get("onto", []),
                json_target=spec.get("json_target", {}),
                algo=algo,
                run=spec.get("run", True),
            )

            node = Node(
                row=pos[0],
                col=pos[1],
                planning_type=planning,
                controlling_type=controlling,
                causal_type=causal,
                pojar=pojar,
                json1={"goal": goal.get("goal", "")},
            )
            landscape.add_node(node)

        return landscape
