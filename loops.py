"""Loop1 (Belief → Measure) and Loop2 (Influence → Measure) helpers.

These are thin wrappers around Node.loop1() and Node.loop2() that can be
called from outside the node (e.g. by the landscape runner).
"""


def run_loop1(node) -> dict:
    """Belief → Measure: node reads json1 as belief, algo produces json2 as measure."""
    return node.loop1()


def run_loop2(node, neighbours: list) -> dict:
    """Influence → Measure: node pushes json2 to neighbours, then re-measures itself."""
    return node.loop2(neighbours)
