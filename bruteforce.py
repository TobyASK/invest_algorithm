from action import Action
import sys

# Stockage du nom du fichier contenant les actions en argument
# avec une valeur par défaut
file = sys.argv[1] if len(sys.argv) > 1 else "action_list.csv"

# Charger les actions
with open(file) as f:
    action_list = []
    f.readline()  # Skipper la ligne d'en-tête
    for line in f:
        name, cost, profit_percent_for_two_years = line.strip().split(",")
        action = Action(name, float(cost),
                        float(profit_percent_for_two_years.strip("%")))
        action_list.append(action)

budget = 500
best_profit = 0
best_combination = []


def calculate_combination_profit(combination):
    total_cost = sum(action.cost for action in combination)
    if total_cost > budget:
        return 0
    total_profit = sum(action.calculate_profit() for action in combination)
    return total_profit


def find_best_combination(current_combination=[], start_index=0):
    global best_profit, best_combination
    current_profit = calculate_combination_profit(current_combination)
    if current_profit > best_profit:
        best_profit = current_profit
        best_combination = current_combination[:]
    for i in range(start_index, len(action_list)):
        current_combination.append(action_list[i])
        find_best_combination(current_combination, i + 1)
        current_combination.pop()


find_best_combination()
print(f"Profit maximal : {best_profit}")

print("Meilleure combinaison d'actions :")
for action in best_combination:
    print(f"- {action.name} (Coût: {action.cost}, "
          f"Profit: {action.calculate_profit()})")
