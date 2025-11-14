"""
Interface graphique pour comparer les algorithmes d'investissement.
Permet d'exécuter et comparer bruteforce vs optimized
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import time
from action import Action

# Import des algorithmes existants
from bruteforce import bruteforce
from optimized import knapsack


class InvestmentGUI:
    """Interface graphique pour AlgoInvest&Trade."""

    def __init__(self, root):
        """Initialise l'interface graphique."""
        self.root = root
        self.root.title("AlgoInvest&Trade - Optimisation d'Investissement")
        self.root.geometry("900x700")

        self.actions = []
        self.budget = 500

        self.setup_ui()

    def setup_ui(self):
        """Création de l'interface utilisateur."""
        # Titre
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)

        title_label = ttk.Label(
            title_frame,
            text="🚀 AlgoInvest&Trade",
            font=("Arial", 20, "bold")
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            title_frame,
            text="Optimisation d'investissement - Période: 2 ans",
            font=("Arial", 10)
        )
        subtitle_label.pack()

        # Section chargement
        load_frame = ttk.LabelFrame(
            self.root,
            text="📁 Données",
            padding="10"
        )
        load_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(
            load_frame,
            text="Charger CSV",
            command=self.load_csv
        ).pack(side=tk.LEFT, padx=5)

        self.file_label = ttk.Label(
            load_frame,
            text="Aucun fichier chargé"
        )
        self.file_label.pack(side=tk.LEFT, padx=10)

        # Budget
        budget_frame = ttk.Frame(load_frame)
        budget_frame.pack(side=tk.RIGHT)

        ttk.Label(budget_frame, text="Budget (€):").pack(side=tk.LEFT)
        self.budget_entry = ttk.Entry(budget_frame, width=10)
        self.budget_entry.insert(0, "500")
        self.budget_entry.pack(side=tk.LEFT, padx=5)

        # Boutons d'exécution
        exec_frame = ttk.LabelFrame(
            self.root,
            text="⚡ Exécution",
            padding="10"
        )
        exec_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(
            exec_frame,
            text="🐌 Force Brute",
            command=self.run_bruteforce,
            width=20
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            exec_frame,
            text="🚀 Optimisé",
            command=self.run_optimized,
            width=20
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            exec_frame,
            text="⚖️ Comparer les deux",
            command=self.run_comparison,
            width=20
        ).pack(side=tk.LEFT, padx=5)

        # Zone de résultats
        results_frame = ttk.LabelFrame(
            self.root,
            text="📊 Résultats",
            padding="10"
        )
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            width=80,
            height=25,
            font=("Consolas", 9)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Barre de statut
        self.status_bar = ttk.Label(
            self.root,
            text="Prêt",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_csv(self):
        """Charge un fichier CSV d'actions."""
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="action_list.csv"
        )

        if not filename:
            return

        try:
            self.actions = []
            with open(filename, 'r', encoding='utf-8') as f:
                f.readline()  # Ignorer l'en-tête
                for line in f:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 3:
                            name = parts[0]
                            cost = float(parts[1])
                            profit_percent = float(parts[2].strip('%'))

                            if cost > 0 and profit_percent >= 0:
                                action = Action(name, cost, profit_percent)
                                self.actions.append(action)

            text = f"{len(self.actions)} actions chargées"
            self.file_label.config(text=text)
            success_msg = f"✅ {filename} chargé avec succès"
            self.status_bar.config(text=success_msg)
            log_text = f"✅ {len(self.actions)} actions chargées " \
                       f"depuis {filename}\n"
            self.log(log_text)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de chargement: {e}")
            self.status_bar.config(text="❌ Erreur de chargement")

    def get_budget(self):
        """Récupère le budget depuis l'interface."""
        try:
            return float(self.budget_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Budget invalide")
            return 500

    def log(self, text):
        """Affiche du texte dans la zone de résultats."""
        self.results_text.insert(tk.END, text)
        self.results_text.see(tk.END)
        self.root.update()

    def clear_results(self):
        """Efface la zone de résultats."""
        self.results_text.delete(1.0, tk.END)

    def bruteforce_algorithm(self, actions, budget):
        """Utilise l'algorithme de force brute depuis bruteforce.py."""
        return bruteforce(actions, budget)

    def optimized_algorithm(self, actions, budget):
        """Utilise l'algorithme optimisé depuis optimized.py."""
        return knapsack(actions, budget)

    def display_results(self, algorithm_name, profit, actions, exec_time):
        """Affiche les résultats d'un algorithme."""
        self.log("=" * 70 + "\n")
        self.log(f"🎯 RÉSULTATS - {algorithm_name}\n")
        self.log("=" * 70 + "\n")
        self.log(f"⏱️  Temps d'exécution: {exec_time:.4f} secondes\n")
        self.log(f"💰 Profit maximal (2 ans): {profit:.2f} €\n")
        self.log(f"📊 Nombre d'actions: {len(actions)}\n")

        total_cost = sum(a.cost for a in actions)
        self.log(f"💵 Coût total: {total_cost:.2f} €\n")

        if total_cost > 0:
            roi = (profit / total_cost) * 100
            self.log(f"📈 ROI (2 ans): {roi:.2f}%\n")

        self.log("\n📋 Actions sélectionnées:\n")
        self.log("-" * 70 + "\n")

        sorted_actions = sorted(
            actions,
            key=lambda x: x.calculate_profit(),
            reverse=True
        )
        for action in sorted_actions:
            action_profit = action.calculate_profit()
            action_percent = action.profit_percent_for_two_years
            log_line = f"  • {action.name:<15} {action.cost:>8.2f}€ → " \
                       f"{action_profit:>8.2f}€ ({action_percent:.1f}%)\n"
            self.log(log_line)

        self.log("\n")

    def run_bruteforce(self):
        """Exécute l'algorithme de force brute."""
        if not self.actions:
            messagebox.showwarning(
                "Attention",
                "Veuillez charger un fichier CSV d'abord"
            )
            return

        budget = self.get_budget()
        self.clear_results()
        status_text = "⏳ Exécution de l'algorithme de force brute..."
        self.status_bar.config(text=status_text)
        self.root.update()

        if len(self.actions) > 25:
            warning_msg = f"Force brute avec {len(self.actions)} " \
                         f"actions peut être très lent.\n" \
                         "Continuer quand même?"
            result = messagebox.askyesno("Attention", warning_msg)
            if not result:
                self.status_bar.config(text="❌ Annulé")
                return

        try:
            start_time = time.time()
            profit, selected = self.bruteforce_algorithm(
                self.actions,
                budget
            )
            exec_time = time.time() - start_time

            self.display_results("FORCE BRUTE", profit, selected, exec_time)
            status_text = f"✅ Force brute terminé en {exec_time:.2f}s"
            self.status_bar.config(text=status_text)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'exécution: {e}")
            self.status_bar.config(text="❌ Erreur")

    def run_optimized(self):
        """Exécute l'algorithme optimisé."""
        if not self.actions:
            messagebox.showwarning(
                "Attention",
                "Veuillez charger un fichier CSV d'abord"
            )
            return

        budget = self.get_budget()
        self.clear_results()
        status_text = "⏳ Exécution de l'algorithme optimisé..."
        self.status_bar.config(text=status_text)
        self.root.update()

        try:
            start_time = time.time()
            profit, selected = self.optimized_algorithm(
                self.actions,
                budget
            )
            exec_time = time.time() - start_time

            self.display_results(
                "ALGORITHME OPTIMISÉ",
                profit,
                selected,
                exec_time
            )
            status_text = f"✅ Optimisé terminé en {exec_time:.2f}s"
            self.status_bar.config(text=status_text)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'exécution: {e}")
            self.status_bar.config(text="❌ Erreur")

    def run_comparison(self):
        """Compare les deux algorithmes."""
        if not self.actions:
            messagebox.showwarning(
                "Attention",
                "Veuillez charger un fichier CSV d'abord"
            )
            return

        budget = self.get_budget()
        self.clear_results()

        if len(self.actions) > 25:
            warning_msg = f"Comparaison avec {len(self.actions)} " \
                         f"actions:\nForce brute peut être très lent.\n" \
                         "Continuer?"
            result = messagebox.askyesno("Attention", warning_msg)
            if not result:
                self.status_bar.config(text="❌ Annulé")
                return

        self.log("=" * 70 + "\n")
        self.log("⚖️  COMPARAISON DES ALGORITHMES\n")
        self.log("=" * 70 + "\n")
        self.log(f"Dataset: {len(self.actions)} actions\n")
        self.log(f"Budget: {budget} €\n\n")

        try:
            # Force brute
            self.status_bar.config(text="⏳ Force brute en cours...")
            self.root.update()

            start_time = time.time()
            bf_profit, bf_actions = self.bruteforce_algorithm(
                self.actions,
                budget
            )
            bf_time = time.time() - start_time

            self.log("🐌 Force Brute:\n")
            self.log(f"   Temps: {bf_time:.4f}s\n")
            self.log(f"   Profit: {bf_profit:.2f}€\n")
            self.log(f"   Actions: {len(bf_actions)}\n\n")

            # Optimisé
            self.status_bar.config(text="⏳ Algorithme optimisé en cours...")
            self.root.update()

            start_time = time.time()
            opt_profit, opt_actions = self.optimized_algorithm(
                self.actions,
                budget
            )
            opt_time = time.time() - start_time

            self.log("🚀 Optimisé:\n")
            self.log(f"   Temps: {opt_time:.4f}s\n")
            self.log(f"   Profit: {opt_profit:.2f}€\n")
            self.log(f"   Actions: {len(opt_actions)}\n\n")

            # Comparaison
            self.log("=" * 70 + "\n")
            self.log("📊 ANALYSE COMPARATIVE\n")
            self.log("=" * 70 + "\n")

            if abs(bf_profit - opt_profit) < 0.01:
                self.log("✅ Résultats identiques (profit optimal)\n")
            else:
                self.log("⚠️  Résultats différents:\n")
                self.log(f"   Force brute: {bf_profit:.2f}€\n")
                self.log(f"   Optimisé: {opt_profit:.2f}€\n")

            if opt_time > 0:
                speedup = bf_time / opt_time
                self.log(f"\n⚡ Accélération: {speedup:.2f}x plus rapide\n")
                time_saved = bf_time - opt_time
                self.log(f"⏱️  Temps économisé: {time_saved:.4f}s\n")

                if bf_time > 0:
                    reduction = ((bf_time - opt_time) / bf_time) * 100
                    self.log(f"📉 Réduction du temps: {reduction:.1f}%\n")

            self.log("\n💡 Complexité théorique:\n")
            n = len(self.actions)
            bf_ops = 2**n
            opt_ops = n * int(budget)
            self.log(f"   Force brute: O(2^{n}) = O({bf_ops:,})\n")
            self.log(f"   Optimisé: O({n} × {int(budget)}) = "
                     f"O({opt_ops:,})\n")

            if opt_ops > 0:
                theoretical_improvement = bf_ops / opt_ops
                self.log(f"   Amélioration théorique: "
                         f"{theoretical_improvement:,.0f}x\n")

            self.status_bar.config(text="✅ Comparaison terminée")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de comparaison: {e}")
            self.status_bar.config(text="❌ Erreur")


def main():
    """Point d'entrée principal."""
    root = tk.Tk()
    InvestmentGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
