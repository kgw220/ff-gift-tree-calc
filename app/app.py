import sys
import os
import streamlit as st

# Get the absolute path to the 'calculations' folder
current_dir = os.path.dirname("app.py")                 
project_root = os.path.abspath(os.path.join(current_dir, ".."))
calculations_path = os.path.join(project_root, "calculations")

# Add 'calculations' to sys.path
sys.path.append(calculations_path)

# Now import the class
from gifttree import gift_tree

st.markdown("""
<style>
@font-face {
  font-family: 'kalyant';
  src: url('kalyant.otf') format('opentype');
}
html, body, [class*="css"] {
  font-family: 'kalyant', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# Streamlit App Title
st.title("Gift Tree Profit Probability Calculator")

# User Inputs
n_trees = st.number_input("Number of Trees Harvested:", min_value=1, value=20)
cost_per_tree = st.number_input("Cost per Tree:", value=1.9e6, format="%.1f")

# Calculate button
if st.button("Compute Probability"):
    gt = gift_tree(n_trees=n_trees, cost_per_tree=cost_per_tree)
    prob_of_profit, fruits, pmf, profits = gt.compute_profit_probability()

    st.markdown(f"### 📊 Probability of Making a Profit: `{prob_of_profit:.4f}`")

    # Summary stats
    summary_stats = gt.get_summary_stats(profits)
    st.markdown(summary_stats)
    st.write(f"Min Profit: {summary_stats['min_profit']:,.0f}")
    st.write(f"Max Profit: {summary_stats['max_profit']:,.0f}")
    st.write(f"Average Profit: {summary_stats['average_profit']:,.0f}")

    # Display the PMF plot
    plot = gt.get_prob_plot(fruits, pmf, profits)
    st.plotly_chart(plot, use_container_width=True)