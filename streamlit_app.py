import streamlit as st
import pandas as pd
import math
import random
import variables
import altair as alt
import numpy as np
from scipy.stats import gaussian_kde

st.set_page_config(
    page_title='Distribution Visualizer',
    page_icon=':earth_americas:',
    layout="wide"
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

def generate_data(variable, n: int) -> list[float]:
    return [variable.generate() for _ in range(n)]

def get_plot(variable, n: int):
    data = generate_data(variable, n)
    avg = sum(data) / len(data)
    
    df = pd.DataFrame(data, columns=['Value'])
    return df, avg

# -----------------------------------------------------------------------------
# Draw the actual page

st.title("Probability Visualizer")
st.write("Browse various probability distributions, including sums, quotients, and products.")

st.header('Distribution', divider='gray')

n = st.slider("Number of Trials", 2, 10000, 1000)

col1, col2 = st.columns([2, 1])

st.session_state.setdefault("selected_variable", None)

with col2:
    st.write("### Variable Configuration")
    
    variable_selected = False
    
    if st.button("Exponential"):
        st.session_state.selected_variable = "exponential"
    if st.button("Uniform"):
        st.session_state.selected_variable = "uniform"
    if st.button("Erlang"):
        st.session_state.selected_variable = "erlang"
    if st.button("Binomial"):
        st.session_state.selected_variable = "binomial"
    if st.button("Poisson"):
        st.session_state.selected_variable = "poisson"
    if st.button("Geometric"):
        st.session_state.selected_variable = "geometric"
    if st.button("Pascal"):
        st.session_state.selected_variable = "pascal"
    
    variable_type = st.session_state.selected_variable
    
    if variable_type:
        variable_selected = True
        if variable_type == "exponential":
            lam = st.slider("Lambda", 0.00001, 1.0, 0.5)
            x = variables.exponential(lam)
        elif variable_type == "uniform":
            a = st.slider("Lower Bound", 0.0, 10.0, 0.0)
            b = st.slider("Upper Bound", 0.0, 10.0, 1.0)
            x = variables.uniform(a, b)
        elif variable_type == "erlang":
            lam = st.slider("Lambda", 0.00001, 1.0, 0.5)
            num = st.slider("Number of Successes", 1, 10, 2)
            x = variables.erlang(lam, num)
        elif variable_type == "binomial":
            p = st.slider("Probability", 0.0, 1.0, 0.5)
            trials = st.slider("Number of Trials", 1, 100, 10)
            x = variables.binomial(trials, p)
        elif variable_type == "poisson":
            lam = st.slider("Lambda", 0.1, 10.0, 1.0)
            x = variables.poisson(lam)
        elif variable_type == "geometric":
            p = st.slider("Probability", 0.0, 1.0, 0.5)
            x = variables.geometric(p)
        elif variable_type == "pascal":
            p = st.slider("Probability", 0.0, 1.0, 0.5)
            l = st.slider("Number of Successes", 1, 10, 2)
            x = variables.pascal(p, l)
        
        df, avg = get_plot(x, n)

with col1:
    if variable_selected:
        st.subheader(f'Average = {avg}')
        
        if x.continous:
            kde = gaussian_kde(df['Value'])
            x_vals = np.linspace(min(df['Value']), max(df['Value']), 200)
            y_vals = kde(x_vals)
            kde_df = pd.DataFrame({'Value': x_vals, 'Density': y_vals})

            chart = alt.Chart(kde_df).mark_line().encode(x='Value', y='Density')
            st.altair_chart(chart, use_container_width=True)
        else:
            hist_df = df['Value'].value_counts().reset_index()
            hist_df.columns = ['Value', 'Count']
            chart = alt.Chart(hist_df).mark_bar().encode(x='Value:O', y='Count')
            st.altair_chart(chart, use_container_width=True)