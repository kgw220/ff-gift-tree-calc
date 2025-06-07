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
mode = st.radio(
    "Display Mode",
    ["Probabilities", "Percentages"],
    horizontal=True
)
mode_convert = {
    "Probabilities": False,
    "Percentages": True,
}   
mode = mode_convert[mode]


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
    plot = gt.get_pmf_plot(fruits, pmf, profits, mode)
    components.html(plot, height=600)