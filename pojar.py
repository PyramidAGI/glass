from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class POJAR:
    """POJAR: ProblemStory, Onto, Json-target, Algo, Run"""
    problem_story: dict = field(default_factory=dict)
    onto: List[str] = field(default_factory=list)
    json_target: dict = field(default_factory=dict)
    algo: Callable[[dict], dict] = field(default=lambda json1: json1)
    run: bool = True
