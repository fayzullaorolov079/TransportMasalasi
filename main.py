"""To'rtta usulni bitta menyudan ishga tushirish."""
from transport_common import *
from potentials import solve as solve_potentials

COSTS = [[4, 6, 8], [5, 3, 7]]
SUPPLY = [40, 60]
DEMAND = [30, 20, 50]

def main():
    print("TRANSPORT MASALASI")
    print("1. Shimoliy-g'arbiy burchak")
    print("2. Eng kichik xarajat")
    print("3. Vogel")
    print("4. Potensiallar usuli (MODI)")
    choice = input("Usulni tanlang (1-4): ").strip()
    costs, supply, demand, note = balance_problem(COSTS, SUPPLY, DEMAND)
    if note:
        print(note)
    if choice == "1":
        plan = initial_plan_northwest(costs, supply, demand)
        display_solution(costs, plan, "Shimoliy-g'arbiy burchak")
    elif choice == "2":
        plan = initial_plan_least_cost(costs, supply, demand)
        display_solution(costs, plan, "Eng kichik xarajat")
    elif choice == "3":
        plan = initial_plan_vogel(costs, supply, demand)
        display_solution(costs, plan, "Vogel")
    elif choice == "4":
        solve_potentials(costs, supply, demand, initial="vogel")
    else:
        print("Noto'g'ri tanlov. 1 dan 4 gacha son kiriting.")

if __name__ == "__main__":
    main()
