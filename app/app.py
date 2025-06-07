import sys
import os
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Importing gift tree module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from calculations.gifttree import gift_tree

st.title("Gift Tree Profit Probability Calculator")

n_trees = st.slider("Number of Gift Trees", min_value=1, max_value=20, value=20, step=1)

gift_tree_seed_cost = st.radio(
    "Gift Tree Seed Cost",
    ["$1,900,000", "$2,000,000", "$2,100,000"],
    horizontal=True
)

# Map display values to numeric values
display_to_value = {
    "$1,900,000": 1900000,
    "$2,000,000": 2000000,
    "$2,100,000": 2100000,
}

cost_per_tree = display_to_value[gift_tree_seed_cost]

# TODO: Update this to show percentages instead of probabilities
if st.button("Compute Probability"):
    gt = gift_tree(n_trees=n_trees, cost_per_tree=cost_per_tree)
    prob_of_profit, fruits, pmf, profits = gt.compute_profit_probability()

    st.markdown(f"### 📊 Probability of Making a Profit: `{prob_of_profit:.4f}`")

    # Summary stats
    summary_stats = gt.get_summary_stats(profits)
    st.write(f"Min Profit: {summary_stats['min_profit']:,.0f} gold")
    st.write(f"Max Profit: {summary_stats['max_profit']:,.0f} gold")
    st.write(f"Average Profit: {summary_stats['average_profit']:,.0f} gold")

    # Display the PMF plot
    plot = gt.get_prob_plot(fruits, pmf, profits)
    components.html(plot, height=600)