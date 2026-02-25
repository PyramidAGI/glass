"""Glass — Node Landscape runner.

Usage:
    python main.py --goal goal_example.json
"""

import argparse
import json
from assembler import GoalAssembler


def main():
    parser = argparse.ArgumentParser(description="Glass: run a node landscape toward a goal.")
    parser.add_argument("--goal", required=True, help="Path to a goal JSON file.")
    parser.add_argument("--verbose", action="store_true", help="Print per-node results.")
    args = parser.parse_args()

    with open(args.goal, "r", encoding="utf-8") as f:
        goal = json.load(f)

    print(f"Goal: {goal.get('goal', '(none)')}")
    print()

    assembler = GoalAssembler()
    landscape = assembler.assemble(goal)
    print(f"Assembled: {landscape}")
    print()
    print("Layout:")
    print(landscape.display())
    print()

    landscape.run()
    print("Execution complete.")
    print()

    if args.verbose:
        for node in sorted(landscape.all_nodes(), key=lambda n: (n.row, n.col)):
            print(f"  {node.label}")
            print(f"    json1 = {node.json1}")
            print(f"    json2 = {node.json2}")
    else:
        nodes = landscape.all_nodes()
        print(f"Processed {len(nodes)} nodes.")
        for node in sorted(nodes, key=lambda n: (n.row, n.col)):
            status = "ran" if node.pojar.run else "skipped"
            print(f"  {node.label} → {status}")


if __name__ == "__main__":
    main()
