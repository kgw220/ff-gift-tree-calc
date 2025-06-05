import numpy as np

class gift_tree:
    """
    Class including methods for calculating and display gift tree profits.
    """

    # Possible outcomes for the number of gift fruit that can occur from a single tree
    fruit_values = [2, 3, 4, 5]

    # Probability of each outcome
    fruit_prob = 0.25

    # Cost of selling a single gift tree fruit
    gift_tree_fruit_sell_price = 0.7e6

    def __init__(self, n_trials: int, cost_per_tree: float = 1.9e6):
        self.n_trials = n_trials
        self.cost_per_tree = cost_per_tree

    def compute_profit_probability(self):
        """
        Compute the probability of making a profit after harvesting a gift tree *n_trials* times.

        Returns:
        - prob_of_profit (float): Probability of making a profit.
        - fruits (np.ndarray): Total fruit count values (x-axis of PMF).
        - pmf (np.ndarray): Probability mass function values for each total fruit count.
        - profits (np.ndarray): Corresponding profit values.
        """

        # PMF for a single event
        single_event_pmf = np.zeros(max(self.fruit_values) + 1)
        for val in self.fruit_values:
            single_event_pmf[val] = self.fruit_prob

        # Convolve the single-event PMF n_trials times
        pmf = single_event_pmf
        for _ in range(self.n_trials - 1):
            pmf = np.convolve(pmf, single_event_pmf)

        # Compute total cost, revenues, and profits
        total_cost = self.n_trials * self.cost_per_tree
        fruits = np.arange(len(pmf))
        revenues = fruits * self.gift_tree_fruit_sell_price
        profits = revenues - total_cost

        # Probability of profit
        prob_of_profit = np.sum(pmf[profits > 0])

        return prob_of_profit, fruits, pmf, profits
