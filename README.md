# AlgoInvest&Trade

Optimisation d'un portefeuille d'investissement sur 2 ans à partir d'un jeu d'actions fourni en CSV. Le projet propose deux approches (force brute et programmation dynamique) et une interface graphique Tkinter permettant de charger un dataset, d'exécuter les deux algorithmes et de comparer leurs performances.

## ✨ Fonctionnalités
- **Algorithme de force brute** (`bruteforce.py`) : explore toutes les combinaisons possibles pour garantir le profit maximal, pratique pour de petits jeux de données (<25 actions).
- **Algorithme optimisé / sac-à-dos** (`optimized.py`) : résolution dynamique en O(n × budget) avec le budget converti en centimes pour éviter les erreurs de flottants.
- **Interface graphique** (`gui.py`) : chargement interactif d'un CSV, paramètres de budget, exécution séparée des deux algorithmes et comparaison détaillée (temps, ROI, coût total, liste triée des actions retenues).
- **Jeux de données d'exemple** :
  - `action_list.csv` (20 lignes) pour tester rapidement.
  - `action_list_new.csv` (1000 lignes) pour évaluer la scalabilité.

## 🏗️ Architecture rapide
| Fichier | Rôle |
| --- | --- |
| `action.py` | Modèle `Action` + calcul du profit sur 2 ans. |
| `bruteforce.py` | Recherche exhaustive de la meilleure combinaison d'actions pour un budget fixé (500 € par défaut). |
| `optimized.py` | Implémentation de l'algorithme du sac-à-dos (programmation dynamique) avec reconstruction de la solution. |
| `gui.py` | Interface Tkinter pour charger un CSV, configurer le budget et comparer les deux approches. |
| `action_list*.csv` | Jeux de données au format `nom,cout,profit%`. |

## ✅ Prérequis
- Python 3.10+ (Tkinter est inclus dans les distributions officielles).
- Aucune dépendance externe supplémentaire.

## 🚀 Installation
```powershell
# Cloner puis aller dans le dossier du projet
git clone https://github.com/TobyASK/invest_algorithm.git
```

## 📦 Jeux de données
- Les fichiers `.csv` doivent comporter un en-tête suivi de lignes `Nom,Coût,Profit%`.
- Les coûts doivent être strictement positifs et les pourcentages exprimés avec le symbole `%` (ex : `53.51,5.19%`).

## 🧪 Utilisation en ligne de commande
Les deux scripts chargent `action_list.csv` par défaut, mais vous pouvez indiquer un autre fichier en premier argument.

### Force brute (petits jeux de données)
```powershell
python bruteforce.py action_list.csv
```

### Programmation dynamique (sac-à-dos)
```powershell
python optimized.py action_list_new.csv
```

> **Remarque :** le budget est fixé à 500 € dans les deux scripts. Ajustez la constante `budget` si nécessaire avant exécution.

Les exécutions affichent :
- le profit total atteint (sur 2 ans)
- le nombre d'actions retenues
- le coût total dépensé
- la liste détaillée des actions sélectionnées avec leur profit individuel.

## 🖥️ Interface graphique
```powershell
python gui.py
```
Fonctionnalités principales :
1. **Chargement CSV** : sélection d'un fichier, validation des données (coût > 0, pourcentage ≥ 0) et indicateur de succès.
2. **Budget personnalisable** : valeur initiale à 500 €, champ modifiable.
3. **Exécution des algorithmes** : boutons dédiés pour Force Brute, Optimisé ou Comparaison complète.
4. **Comparateur visuel** : temps d'exécution, profits, ROI, coûts et liste triée des actions retenues.
5. **Alertes** : avertissement si la force brute est lancée sur plus de 25 actions.

## 📊 Performances & limites
- **Force brute** : complexité O(2^n). À réserver aux petits jeux de données, sinon l'application affiche un avertissement.
- **Optimisé** : complexité O(n × budget). Convertir le budget en centimes garantit une meilleure précision mais augmente la taille de la table DP (ex : 500 € → 50 000 colonnes).
- **Jeux de données volumineux** : le CSV de 1000 lignes permet d'évaluer la différence de temps entre les deux approches directement via la GUI.

## 🔧 Prochaines améliorations possibles
- Paramétrage du budget et des fichiers directement via la ligne de commande (arguments `--file`, `--budget`, etc.).
- Export des résultats (JSON/CSV) depuis la CLI et la GUI.
- Ajout de tests unitaires pour sécuriser les calculs de profits et la reconstruction des solutions.

## 📄 Licence
Aucune licence explicite dans le dépôt. Ajoutez un `LICENSE` si vous souhaitez partager ou réutiliser ce code publiquement.
