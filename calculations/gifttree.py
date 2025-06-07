import numpy as np
import plotly.graph_objects as go
import base64

from PIL import Image
from io import BytesIO
from pathlib import Path

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

    def __init__(self, n_trees: int, cost_per_tree: float = 1.9e6):
        self.n_trees = n_trees
        self.cost_per_tree = cost_per_tree

    def compute_profit_probability(self):
        """
        Compute the probability of making a profit after harvesting n gift trees.

        Returns:
        - prob_of_profit (float): Probability of making a profit.
        - fruits (np.ndarray): Total fruit count values (x-axis of PMF).
        - pmf (np.ndarray): Probability mass function values for each total fruit count.
        - profits (np.ndarray): Corresponding profit values.
        """

        # PMF for a single tree
        single_event_pmf = np.zeros(max(self.fruit_values) + 1)
        for val in self.fruit_values:
            single_event_pmf[val] = self.fruit_prob

        # Convolve the single-event PMF for n_trees to get the PMF for all possible total fruits
        pmf = single_event_pmf
        for _ in range(self.n_trees - 1):
            pmf = np.convolve(pmf, single_event_pmf)

        # Compute total cost, revenues, and profits
        total_cost = self.n_trees * self.cost_per_tree
        fruits = np.arange(len(pmf))
        revenues = fruits * self.gift_tree_fruit_sell_price
        profits = revenues - total_cost

        # Calculate the probability of profit
        prob_of_profit = np.sum(pmf[profits > 0])

        # Update profits/pmf/fruits to remove the unrealistic values, since the range encomposed
        # all possible fruit values, but we only care about the ones that are realistic
        min_total_fruit = self.n_trees * min(self.fruit_values)
        remove_count = sum(x < min_total_fruit for x in fruits)
        fruits = fruits[remove_count:]
        profits = profits[remove_count:]
        pmf = pmf[remove_count:]

        return prob_of_profit, fruits, pmf, profits
    

    def get_summary_stats(self, profits: np.array) -> dict:
        """
        Calculate summary statistics for the profits.

        Parameters:
        - profits: np.ndarray
            Array of profit values.

        Returns:
        - dict:
            Dictionary containing min, max, and average profit.
        """
        
        min_profit = profits.min()
        max_profit = profits.max()
        mean_profit = profits.mean()
        
        return {
            'min_profit': min_profit,
            'max_profit': max_profit,
            'average_profit': mean_profit
        }
    

    # TODO: Update this so background is transparent and font is correctly set
    def get_prob_plot(self, fruits: np.array, pmf: np.array, profits: np.array) -> go.Figure:
        """
        Generate a plot of the probability mass function (PMF) for the total fruit count.

        Parameters:
        - fruits: np.ndarray
            Total fruit count values (x-axis of PMF); returned from compute_profit_probability.
        - pmf: np.ndarray
            Probability mass function values for each total fruit count; returned from 
            compute_profit_probability.
        - profits: np.ndarray
            Corresponding profit values; returned from compute_profit_probability.

        Returns:
        - go.Figure:
            A Plotly figure object containing the PMF plot.
        """

        # Compute the minimum number of fruits needed to break even
        break_even_fruit_count = np.min(fruits[profits > 0])

        # Create Plotly bar chart
        fig = go.Figure()

        # PMF bars
        fig.add_trace(go.Bar(
            x=fruits,
            y=pmf,
            name='Probability Mass Function',
            marker_color='royalblue',
            showlegend=False
        ))

        # Vertical line at break-even point
        fig.add_trace(go.Scatter(
            x=[break_even_fruit_count, break_even_fruit_count],
            y=[0, max(pmf)],
            mode='lines',
            name='Profit Threshold',
            line=dict(color='red', dash='dash')
        ))

        # Embedding background image
        img = Image.open("assets/garden.jpg")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        encoded_image = base64.b64encode(buffer.getvalue()).decode()
        img_uri = "data:image/png;base64," + encoded_image

        # Defining custom css for the font
        with open("../app/assets/Kalyant Demo-Bold.otf", "rb") as f:
            font_base64 = base64.b64encode(f.read()).decode("utf-8")

        font_css = f"""
                    <style>
                    @font-face {{
                        font-family: 'KalyantBold';
                        src: url(data:font/opentype;base64,{font_base64}) format('opentype');
                    }}
                    </style>
                    """
        # Layout
        fig.update_layout(
            title=f'Probability of Total Fruits for {self.n_trees} Gift Trees',
            xaxis_title='Total Fruit Count',
            yaxis_title='Probability',
            showlegend=True,
            font=dict(
                family="KalyantBold",  
                size=18,
                color="black"
            ),
            images=[dict(
                source=img_uri,
                xref="paper",
                yref="paper",
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                xanchor="left",
                yanchor="top",
                sizing="stretch",
                opacity=0.3,
                layer="below"
            )]
        )

        # Convert to HTML
        html = font_css + fig.to_html(include_plotlyjs='cdn')

        return html
