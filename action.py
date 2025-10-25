class Action:
    def __init__(self, name, cost, profit_percent_for_two_years):
        self.name = name
        self.cost = cost
        self.profit_percent_for_two_years = profit_percent_for_two_years

    def calculate_profit(self):
        return self.cost * (self.profit_percent_for_two_years / 100)

    def __repr__(self):
        return (f"Action(name={self.name}, cost={self.cost}, "
                f"profit_percent_for_two_years="
                f"{self.profit_percent_for_two_years})")
