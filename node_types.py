from enum import Enum


class PlanningType(Enum):
    NAVIGATOR = "navigator"
    PLANNER = "planner"
    SCHEDULER = "scheduler"


class ControllingType(Enum):
    CONTROLLER = "controller"
    REGULATOR = "regulator"
    MONITOR = "monitor"


class CausalType(Enum):
    CAUSAL = "causal"
    REACTIVE = "reactive"
    PREDICTIVE = "predictive"
