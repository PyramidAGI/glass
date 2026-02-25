# Glass

A Python system that arranges processing nodes in a staggered chessboard grid. Each node transforms JSON input into JSON output via a user-supplied algorithm, following the **POJAR** framework. Specify a goal as JSON and the system automatically assembles the required nodes and runs them.

## Concepts

### Node landscape
Nodes are placed at chessboard-black-square positions in a 2D grid — i.e. positions `(row, col)` where `(row + col) % 2 == 0`. Neighbours are the four diagonally adjacent cells. Information flows **down** (parent → child) and **up** (child → parent) through the landscape.

### Node types
Each node has three orthogonal type dimensions:

| Dimension | Options |
|-----------|---------|
| Planning | `navigator`, `planner`, `scheduler` |
| Controlling | `controller`, `regulator`, `monitor` |
| Causal | `causal`, `reactive`, `predictive` |

The **navigator node** (`navigator / controller / causal`) is the default multi-purpose combination.

### POJAR
Every node is driven by a POJAR record:

| Field | Type | Description |
|-------|------|-------------|
| `ProblemStory` | `dict` | JSON describing the problem this node addresses |
| `Onto` | `List[str]` | Ontology / vocabulary for the node |
| `Json-target` | `dict` | Desired output state |
| `Algo` | `Callable` | Python function: `json1 → json2` |
| `Run` | `bool` | Whether to execute this node |

### Loops
Each node runs two feedback loops:

- **Loop 1 — Belief → Measure**: the node treats `json1` as its current belief, runs `Algo`, and stores the result as `json2`.
- **Loop 2 — Influence → Measure**: the node pushes its `json2` as an influence signal to its neighbours, then re-measures its own state.

## Usage

```bash
python main.py --goal goal_example.json
python main.py --goal goal_example.json --verbose
```

## Goal JSON schema

```json
{
  "goal": "Description of the overall objective",
  "grid_size": [4, 4],
  "required_node_types": [
    {
      "planning": "navigator",
      "controlling": "controller",
      "causal": "causal",
      "problem_story": {},
      "onto": ["keyword1", "keyword2"],
      "json_target": { "done": true },
      "algo": { "type": "passthrough" },
      "run": true
    }
  ],
  "constraints": {}
}
```

### Algo types

| Type | Description |
|------|-------------|
| `passthrough` | Returns `json1` unchanged (default) |
| `merge` | Merges a `data` dict into `json1` |
| `inline` | Evaluates a Python lambda string, e.g. `"lambda j: {**j, 'done': True}"` |

## File structure

```
glass/
├── main.py            # CLI entry point
├── assembler.py       # GoalAssembler: goal JSON → NodeLandscape
├── landscape.py       # NodeLandscape: chessboard grid, propagation, run loop
├── node.py            # Node class: position, types, POJAR, loop1/loop2
├── node_types.py      # PlanningType, ControllingType, CausalType enums
├── pojar.py           # POJAR dataclass
├── loops.py           # run_loop1 / run_loop2 helpers
└── goal_example.json  # Example goal specification
```
