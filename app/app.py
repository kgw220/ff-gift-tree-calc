"""
Sample streamlit app for the Gift Tree Profit Probability Calculator.
"""

import sys
import os
import streamlit as st
import streamlit.components.v1 as components

# Importing gift tree module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from calculations.gifttree import gift_tree

st.sidebar.header("Gift Tree Profit Probability Calculator")

# Input for number of gift trees
n_trees = st.sidebar.slider("Number of Gift Trees", min_value=1, max_value=20, value=20, step=1)

# Selection for cost of gift tree seeds
cost_per_tree = st.sidebar.radio(
    "Gift Tree Seed Cost", ["$1,900,000", "$2,000,000", "$2,100,000"], horizontal=True
)
gift_tree_cost_convert = {
    "$1,900,000": 1900000,
    "$2,000,000": 2000000,
    "$2,100,000": 2100000,
}
cost_per_tree = gift_tree_cost_convert[cost_per_tree]

# Mode selection on rather user wants to see probabilities or percentages
mode_label = st.sidebar.radio("Display Mode", ["Probability", "Percentage"], horizontal=True)
mode_convert = {
    "Probability": False,
    "Percentage": True,
}
mode = mode_convert[mode_label]

# Calculate and display everything with the user chosen options
gt = gift_tree(n_trees=n_trees, cost_per_tree=cost_per_tree)
prob_of_profit, fruits, pmf, profits = gt.compute_profit_probability()

# If percentages are selected, show percentage of making profit. Otherwise, show probability.
if mode:
    st.sidebar.markdown(
        f"{mode_label} of making a profit from {n_trees} tree(s): `{prob_of_profit * 100:.4f}%`"
    )
else:
    st.sidebar.markdown(
        f"{mode_label} of making a profit from {n_trees} tree(s): `{prob_of_profit:.4f}`"
    )

# Display summary statistics
st.sidebar.markdown(f"Min Profit: {gt.get_min(profits):,.0f} gold")
st.sidebar.markdown(f"Max Profit: {gt.get_max(profits):,.0f} gold")
st.sidebar.markdown(f"Average Profit: {gt.get_average(profits):,.0f} gold")

# Display the PMF plot
plot = gt.get_pmf_plot(fruits=fruits, pmf=pmf, profits=profits, percent=mode)
components.html(plot, height=600)
