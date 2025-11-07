from action import Action
import sys

# Stockage du nom du fichier contenant les actions en argument
# avec une valeur par défaut
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


# Algorithme du sac-à-dos
def knapsack(actions, budget):
    n = len(actions)
    budget_cents = int(budget * 100)  # Convertir en centimes
    # Initialiser la table DP : dp[i][w] = profit maximal avec les i premières
    # actions et budget w centimes
    dp = [[0 for w in range(budget_cents + 1)] for i in range(n + 1)]
    # Remplir la table
    for i in range(1, n + 1):
        action = actions[i - 1]  # On initialise avec la première action
        cost_cents = int(action.cost * 100)  # Coût des actions en centimes
        profit = action.calculate_profit()  # Profit généré par l'action
        for w in range(budget_cents + 1):
            dp[i][w] = dp[i - 1][w]  # Ne pas prendre
            if cost_cents <= w:
                dp[i][w] = max(dp[i][w], (dp[i - 1][w - cost_cents] + profit))
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
# On affiche le profit max en euros avec centimes
print(f"Profit maximal (2 ans): {max_profit:.2f} €")
# On affiche le nombre d'actions selectionnées
print(f"Nombre d'actions: {len(selected_actions)}")
# On affiche le coût total avec la somme des coûts de chaque action
print(f"Coût total: {sum(a.cost for a in selected_actions):.2f} €")

# On affiche chacunes des actions selectionnées
print("\nActions sélectionnées:")
for action in selected_actions:
    profit = action.calculate_profit()
    # On affiche le nom, le coût et le profit en euros
    print(f"- {action.name}: {action.cost}€ → {profit:.2f}€")
