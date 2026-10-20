"""Umumiy yordamchi funksiyalar: transport jadvali, tekshiruv va xarajat."""
from typing import List, Tuple, Optional

Matrix = List[List[float]]

def validate_problem(costs: Matrix, supply: List[float], demand: List[float]) -> None:
    if not costs or not costs[0]:
        raise ValueError("Xarajatlar jadvali bo'sh bo'lmasligi kerak.")
    if len(costs) != len(supply):
        raise ValueError("Xarajatlar qatorlari soni supply uzunligiga teng bo'lishi kerak.")
    n = len(costs[0])
    if len(demand) != n:
        raise ValueError("Xarajatlar ustunlari soni demand uzunligiga teng bo'lishi kerak.")
    if any(len(row) != n for row in costs):
        raise ValueError("Xarajatlar jadvalining barcha qatorlari bir xil uzunlikda bo'lishi kerak.")
    if any(x < 0 for row in costs for x in row):
        raise ValueError("Transport xarajatlari manfiy bo'lmasligi kerak.")
    if any(x < 0 for x in supply) or any(x < 0 for x in demand):
        raise ValueError("Ta'minot va talab manfiy bo'lmasligi kerak.")

def balance_problem(costs: Matrix, supply: List[float], demand: List[float]):
    """Ochiq masalani nol xarajatli soxta qator/ustun qo'shib yopiq qiladi."""
    costs = [row[:] for row in costs]
    supply = supply[:]
    demand = demand[:]
    total_s, total_d = sum(supply), sum(demand)
    if abs(total_s - total_d) < 1e-9:
        return costs, supply, demand, None
    if total_s < total_d:
        costs.append([0.0] * len(demand))
        supply.append(total_d - total_s)
        return costs, supply, demand, f"Soxta ta'minotchi qo'shildi: {total_d-total_s:g} birlik."
    costs = [row + [0.0] for row in costs]
    demand.append(total_s - total_d)
    return costs, supply, demand, f"Soxta iste'molchi qo'shildi: {total_s-total_d:g} birlik."

def total_cost(costs: Matrix, plan: Matrix) -> float:
    return sum(costs[i][j] * plan[i][j]
               for i in range(len(costs)) for j in range(len(costs[0])))

def print_matrix(title: str, matrix: Matrix, row_prefix="A", col_prefix="B") -> None:
    print(f"\n{title}")
    print("       " + "".join(f"{col_prefix}{j+1:>9}" for j in range(len(matrix[0]))))
    for i, row in enumerate(matrix):
        print(f"{row_prefix}{i+1:<5}" + "".join(f"{v:9.2f}" for v in row))

def print_problem(costs: Matrix, supply: List[float], demand: List[float]) -> None:
    print("Xarajatlar jadvali (oxirgi ustun — ta'minot, oxirgi qator — talab):")
    print("       " + "".join(f"B{j+1:>9}" for j in range(len(demand))) + "  Ta'minot")
    for i, row in enumerate(costs):
        print(f"A{i+1:<5}" + "".join(f"{v:9.2f}" for v in row) + f"{supply[i]:10.2f}")
    print("Talab " + "".join(f"{v:9.2f}" for v in demand) + f"{sum(demand):10.2f}")

def initial_plan_northwest(costs: Matrix, supply: List[float], demand: List[float]) -> Matrix:
    """Shimoliy-g'arbiy burchak usuli."""
    s, d = supply[:], demand[:]
    m, n = len(s), len(d)
    plan = [[0.0] * n for _ in range(m)]
    i = j = 0
    while i < m and j < n:
        q = min(s[i], d[j])
        plan[i][j] = q
        s[i] -= q
        d[j] -= q
        s_done = abs(s[i]) < 1e-9
        d_done = abs(d[j]) < 1e-9
        if s_done and d_done:
            # Diagonal move; degeneracy is handled later by MODI using a spanning tree.
            i += 1
            j += 1
        elif s_done:
            i += 1
        else:
            j += 1
    return plan

def initial_plan_least_cost(costs: Matrix, supply: List[float], demand: List[float]) -> Matrix:
    """Eng kichik xarajatlar usuli; tenglikda birinchi uchragan katak tanlanadi."""
    s, d = supply[:], demand[:]
    m, n = len(s), len(d)
    plan = [[0.0] * n for _ in range(m)]
    active_rows, active_cols = set(range(m)), set(range(n))
    while active_rows and active_cols:
        candidates = [(costs[i][j], i, j) for i in active_rows for j in active_cols]
        _, i, j = min(candidates)
        q = min(s[i], d[j])
        plan[i][j] += q
        s[i] -= q
        d[j] -= q
        row_done, col_done = abs(s[i]) < 1e-9, abs(d[j]) < 1e-9
        if row_done:
            active_rows.discard(i)
        if col_done:
            active_cols.discard(j)
        # If both finish, removing both is valid; any degeneracy is handled by MODI.
    return plan

def initial_plan_vogel(costs: Matrix, supply: List[float], demand: List[float]) -> Matrix:
    """Vogel approksimatsiya usuli (VAM)."""
    s, d = supply[:], demand[:]
    m, n = len(s), len(d)
    plan = [[0.0] * n for _ in range(m)]
    active_rows, active_cols = set(range(m)), set(range(n))
    while active_rows and active_cols:
        penalties = []
        for i in active_rows:
            vals = sorted(costs[i][j] for j in active_cols)
            penalty = vals[1] - vals[0] if len(vals) >= 2 else vals[0]
            penalties.append((penalty, "r", i, min(active_cols, key=lambda j: costs[i][j])))
        for j in active_cols:
            vals = sorted(costs[i][j] for i in active_rows)
            penalty = vals[1] - vals[0] if len(vals) >= 2 else vals[0]
            penalties.append((penalty, "c", j, min(active_rows, key=lambda i: costs[i][j])))
        # Highest penalty; on tie choose candidate with smallest cell cost.
        max_penalty = max(p[0] for p in penalties)
        tied = [p for p in penalties if abs(p[0] - max_penalty) < 1e-9]
        penalty, kind, idx, best_idx = min(tied, key=lambda p: costs[p[2]][p[3]] if p[1] == "r" else costs[p[3]][p[2]])
        i, j = (idx, best_idx) if kind == "r" else (best_idx, idx)
        q = min(s[i], d[j])
        plan[i][j] += q
        s[i] -= q
        d[j] -= q
        if abs(s[i]) < 1e-9:
            active_rows.discard(i)
        if abs(d[j]) < 1e-9:
            active_cols.discard(j)
    return plan

def display_solution(costs: Matrix, plan: Matrix, title="Reja") -> None:
    print_matrix(title, plan)
    print(f"Jami transport xarajati: {total_cost(costs, plan):g}")
