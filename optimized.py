from action import Action
import sys

file = sys.argv[1] if len(sys.argv) > 1 else "action_list.csv"

# Charger les actions
with open(file) as f:
    actions = []
    f.readline()  # Ignorer l'en-tête
    for line in f:
        name, cost, profit_percent = line.strip().split(",")
        action = Action(name, float(cost), float(profit_percent.strip("%")))
        actions.append(action)

budget = 500


# Algorithme optimisé (programmation dynamique)
def knapsack(actions, budget):
    n = len(actions)
    budget_cents = int(budget * 100)  # Convertir en centimes
    # Initialiser la table DP : dp[i][w] = profit maximal avec les i premières
    # actions et budget w centimes
    dp = [[0 for w in range(budget_cents + 1)] for i in range(n + 1)]
    # Remplir la table
    for i in range(1, n + 1):
        action = actions[i - 1]
        cost_cents = int(action.cost * 100)
        profit = action.calculate_profit()
        for w in range(budget_cents + 1):
            dp[i][w] = dp[i - 1][w]  # Ne pas prendre
            if cost_cents <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - cost_cents] + profit)
    # Retrouver les actions sélectionnées
    selected = []
    w = budget_cents
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(actions[i - 1])
            w -= int(actions[i - 1].cost * 100)
    return dp[n][budget_cents], selected


# Exécution
max_profit, selected_actions = knapsack(actions, budget)

# Affichage des résultats
print(f"Profit maximal (2 ans): {max_profit:.2f} €")
print(f"Nombre d'actions: {len(selected_actions)}")
print(f"Coût total: {sum(a.cost for a in selected_actions):.2f} €")

print("\nActions sélectionnées:")
for action in selected_actions:
    profit = action.calculate_profit()
    print(f"- {action.name}: {action.cost}€ → {profit:.2f}€")
