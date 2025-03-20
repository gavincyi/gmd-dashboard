import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Crisis Comparison", layout="wide")

def load_data():
    df = pd.read_csv('GMD.csv')
    return df

st.title("🔄 Crisis Comparison Analysis")
st.write("Compare economic indicators before, during, and after crisis periods")

# Load the data
df = load_data()

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    
    # Crisis type selection
    crisis_types = {
        'Sovereign Debt Crisis': 'SovDebtCrisis',
        'Currency Crisis': 'CurrencyCrisis',
        'Banking Crisis': 'BankingCrisis'
    }
    selected_crisis = st.selectbox(
        'Select Crisis Type',
        list(crisis_types.keys())
    )
    
    # Time window
    window_size = st.slider(
        'Years around crisis (±)',
        min_value=1,
        max_value=5,
        value=3
    )

# Process data
crisis_col = crisis_types[selected_crisis]
crisis_instances = df[df[crisis_col] == 1][['countryname', 'year']]

# Create analysis dataframes
all_windows = []
for _, crisis in crisis_instances.iterrows():
    country = crisis['countryname']
    crisis_year = crisis['year']
    
    # Get window of years around crisis
    window = df[
        (df['countryname'] == country) &
        (df['year'] >= crisis_year - window_size) &
        (df['year'] <= crisis_year + window_size)
    ].copy()
    
    if len(window) == (2 * window_size + 1):  # Only include complete windows
        window['years_from_crisis'] = window['year'] - crisis_year
        all_windows.append(window)

if all_windows:
    analysis_df = pd.concat(all_windows)
    
    # Calculate averages
    avg_df = analysis_df.groupby('years_from_crisis').agg({
        'rGDP': 'mean',
        'infl': 'mean',
        'unemp': 'mean',
        'REER': 'mean',
        'govdebt_GDP': 'mean',
        'CA_GDP': 'mean'
    }).reset_index()
    
    # Create visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Real GDP and Inflation
        fig1 = make_subplots(rows=2, cols=1, 
                           subplot_titles=('Average Real GDP', 'Average Inflation'))
        
        fig1.add_trace(
            go.Scatter(x=avg_df['years_from_crisis'], y=avg_df['rGDP'],
                      name='Real GDP'),
            row=1, col=1
        )
        
        fig1.add_trace(
            go.Scatter(x=avg_df['years_from_crisis'], y=avg_df['infl'],
                      name='Inflation'),
            row=2, col=1
        )
        
        fig1.update_layout(height=600, showlegend=True,
                         xaxis_title='Years from Crisis',
                         xaxis2_title='Years from Crisis')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Government Debt and Current Account
        fig2 = make_subplots(rows=2, cols=1,
                           subplot_titles=('Government Debt (% of GDP)', 
                                         'Current Account (% of GDP)'))
        
        fig2.add_trace(
            go.Scatter(x=avg_df['years_from_crisis'], y=avg_df['govdebt_GDP'],
                      name='Government Debt'),
            row=1, col=1
        )
        
        fig2.add_trace(
            go.Scatter(x=avg_df['years_from_crisis'], y=avg_df['CA_GDP'],
                      name='Current Account'),
            row=2, col=1
        )
        
        fig2.update_layout(height=600, showlegend=True,
                         xaxis_title='Years from Crisis',
                         xaxis2_title='Years from Crisis')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Crisis Frequency Table
    st.subheader("Crisis Frequency by Country")
    crisis_freq = crisis_instances['countryname'].value_counts().reset_index()
    crisis_freq.columns = ['Country', 'Number of Crises']
    st.dataframe(crisis_freq)
    
else:
    st.warning("No crisis episodes found with complete data for the selected window size.") 