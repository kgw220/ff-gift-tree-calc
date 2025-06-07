import sys
import os
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Importing gift tree module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from calculations.gifttree import gift_tree

# Step 3: Read base64 string from file
cwd = os.getcwd()
st.markdown(cwd)
font_b64_path = Path("font_base64.txt")  
font_base64 = "".join(Path("font_base64.txt").read_text(encoding="utf-8").splitlines()).strip()


# Step 4: Define @font-face CSS with the embedded base64 font
font_css = f"""
<style>
@font-face {{
    font-family: 'KalyantBold';
    src: url(data:font/opentype;base64,{font_base64}) format('opentype');
}}
body, .plotly-chart text {{
    font-family: 'KalyantBold', sans-serif;
}}
</style>
"""

# Step 5: Inject into Streamlit
st.markdown(font_css, unsafe_allow_html=True)

st.title("Gift Tree Profit Probability Calculator")

n_trees = st.slider("Number of Gift Trees", min_value=1, max_value=20, value=20, step=1)

# NOTE: Probably better at separate buttons since there are only three options
cost_per_tree = st.slider("Cost of Gift Tree Seed", min_value=1_900_000, max_value=2_100_000, value=(1_900_000), step=100_000)

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