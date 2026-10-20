"""Shimoliy-g'arbiy burchak usuli."""
from transport_common import *

COSTS = [[4, 6, 8], [5, 3, 7]]
SUPPLY = [40, 60]
DEMAND = [30, 20, 50]

def solve(costs=COSTS, supply=SUPPLY, demand=DEMAND):
    validate_problem(costs, supply, demand)
    costs, supply, demand, note = balance_problem(costs, supply, demand)
    if note:
        print(note)
    plan = initial_plan_northwest(costs, supply, demand)
    display_solution(costs, plan, "Shimoliy-g'arbiy burchak usuli natijasi")
    return plan

if __name__ == "__main__":
    solve()
