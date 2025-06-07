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

# Selection for cost of gift tree seeds
cost_per_tree = st.radio(
    "Gift Tree Seed Cost",
    ["$1,900,000", "$2,000,000", "$2,100,000"],
    horizontal=True
)
gift_tree_cost_convert = {
    "$1,900,000": 1900000,
    "$2,000,000": 2000000,
    "$2,100,000": 2100000,
}
cost_per_tree = gift_tree_cost_convert[cost_per_tree]

# Mode selection on rather user wants to see probabilities or percentages
mode_label = st.radio(
    "Display Mode",
    ["Probability", "Percentage"],
    horizontal=True
)
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
    st.markdown(f"### {mode_label} of making a profit from {n_trees} tree(s): `{prob_of_profit * 100:.4f}%`")
else:
    st.markdown(f"### {mode_label} of making a profit from {n_trees} tree(s): `{prob_of_profit:.4f}`")

# Summary stats
summary_stats = gt.get_summary_stats(profits)
st.markdown(f"#### Min Profit: {summary_stats['min_profit']:,.0f} gold")
st.markdown(f"#### Max Profit: {summary_stats['max_profit']:,.0f} gold")
st.markdown(f"#### Average Profit: {summary_stats['average_profit']:,.0f} gold")

# Display the PMF plot
plot = gt.get_pmf_plot(fruits, pmf, profits, mode)
components.html(plot, height=600)