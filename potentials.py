"""Potensiallar usuli (MODI): boshlang'ich rejani optimalgacha yaxshilash."""
from transport_common import *

EPS = 1e-9

def _basis_tree(plan):
    """Nol bo'lmagan kataklardan bazis tuzadi; zarur bo'lsa epsilon-bazis katak qo'shadi."""
    m, n = len(plan), len(plan[0])
    basis = {(i, j) for i in range(m) for j in range(n) if plan[i][j] > EPS}
    target = m + n - 1

    # Union-find orqali sikl hosil qilmaydigan nol kataklarni bazisga qo'shamiz.
    parent = list(range(m + n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[rb] = ra
        return True

    for i, j in sorted(basis):
        union(i, m + j)
    for i in range(m):
        for j in range(n):
            if len(basis) >= target:
                break
            if (i, j) not in basis and union(i, m + j):
                basis.add((i, j))
        if len(basis) >= target:
            break
    if len(basis) != target:
        raise RuntimeError("Bazisni tuzib bo'lmadi; boshlang'ich reja tekshirilishi kerak.")
    return basis

def _potentials(costs, basis):
    m, n = len(costs), len(costs[0])
    u, v = [None]*m, [None]*n
    u[0] = 0.0
    changed = True
    while changed:
        changed = False
        for i, j in basis:
            if u[i] is not None and v[j] is None:
                v[j] = costs[i][j] - u[i]
                changed = True
            elif v[j] is not None and u[i] is None:
                u[i] = costs[i][j] - v[j]
                changed = True
    if any(x is None for x in u) or any(x is None for x in v):
        raise RuntimeError("Bazis bog'lanmagan; potensiallarni topib bo'lmadi.")
    return u, v

def _find_cycle(basis, entering, m, n):
    """Entering katakni qo'shib hosil bo'lgan siklni DFS bilan topadi."""
    cells = set(basis)
    cells.add(entering)
    start = entering

    def dfs(cell, path, used_rows, used_cols, move_row):
        i, j = cell
        if move_row:
            candidates = [(i, jj) for jj in range(n) if jj != j and (i, jj) in cells]
        else:
            candidates = [(ii, j) for ii in range(m) if ii != i and (ii, j) in cells]
        for nxt in candidates:
            if nxt == start and len(path) >= 4 and len(path) % 2 == 0:
                return path + [start]
            if nxt in path:
                continue
            result = dfs(nxt, path + [nxt], used_rows, used_cols, not move_row)
            if result:
                return result
        return None

    cycle = dfs(start, [start], set(), set(), True)
    if cycle is None:
        cycle = dfs(start, [start], set(), set(), False)
    if cycle is None:
        raise RuntimeError("Yopiq sikl topilmadi.")
    return cycle[:-1]  # start takrorlanishini olib tashlash

def solve(costs=None, supply=None, demand=None, initial="vogel", max_iterations=1000, verbose=True):
    if costs is None:
        costs = [[4, 6, 8], [5, 3, 7]]
    if supply is None:
        supply = [40, 60]
    if demand is None:
        demand = [30, 20, 50]
    validate_problem(costs, supply, demand)
    costs, supply, demand, note = balance_problem(costs, supply, demand)
    if note and verbose:
        print(note)

    methods = {
        "northwest": initial_plan_northwest,
        "least_cost": initial_plan_least_cost,
        "vogel": initial_plan_vogel,
    }
    if initial not in methods:
        raise ValueError("initial: 'northwest', 'least_cost' yoki 'vogel' bo'lishi kerak.")
    plan = methods[initial](costs, supply, demand)
    m, n = len(costs), len(costs[0])

    for iteration in range(1, max_iterations + 1):
        basis = _basis_tree(plan)
        u, v = _potentials(costs, basis)
        deltas = {(i, j): costs[i][j] - (u[i] + v[j])
                  for i in range(m) for j in range(n) if (i, j) not in basis}
        if not deltas or min(deltas.values()) >= -EPS:
            if verbose:
                print(f"\nOptimal reja topildi. Iteratsiyalar: {iteration-1}")
                print("u potensiallari:", [round(x, 6) for x in u])
                print("v potensiallari:", [round(x, 6) for x in v])
                display_solution(costs, plan, "Optimal transport rejasi")
            return plan

        entering = min(deltas, key=deltas.get)
        cycle = _find_cycle(basis, entering, m, n)
        minus_cells = [cycle[k] for k in range(1, len(cycle), 2)]
        theta = min(plan[i][j] for i, j in minus_cells)

        # Reja miqdorlarini sikl bo'yicha +/- theta o'zgartirish.
        for k, (i, j) in enumerate(cycle):
            if k % 2 == 0:
                plan[i][j] += theta
            else:
                plan[i][j] -= theta
                if abs(plan[i][j]) < EPS:
                    plan[i][j] = 0.0

        if verbose:
            print(f"Iteratsiya {iteration}: kiruvchi katak A{entering[0]+1}-B{entering[1]+1}, "
                  f"bahosi {deltas[entering]:g}, theta={theta:g}")
    raise RuntimeError("Maksimal iteratsiya soniga yetildi; yechim tekshirilishi kerak.")

if __name__ == "__main__":
    solve()
