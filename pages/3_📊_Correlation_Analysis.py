import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

st.set_page_config(page_title="Correlation Analysis", layout="wide")

def load_data():
    df = pd.read_csv('GMD.csv')
    return df

st.title("📊 Correlation Analysis")
st.write("Analyze relationships between different economic indicators")

# Load the data
df = load_data()

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    
    # Country selection
    available_countries = sorted(df['countryname'].unique())
    selected_countries = st.multiselect(
        'Select Countries',
        available_countries,
        default=['United States', 'China', 'Japan', 'Germany', 'United Kingdom']
    )
    
    # Indicator selection
    indicators = {
        'Real GDP Growth': 'rGDP',
        'Inflation': 'infl',
        'Unemployment': 'unemp',
        'Government Debt (% of GDP)': 'govdebt_GDP',
        'Current Account (% of GDP)': 'CA_GDP',
        'Investment (% of GDP)': 'inv_GDP',
        'Real Exchange Rate': 'REER',
        'Short-term Interest Rate': 'strate'
    }
    
    x_indicator = st.selectbox(
        'Select X-axis Indicator',
        list(indicators.keys()),
        index=0
    )
    
    y_indicator = st.selectbox(
        'Select Y-axis Indicator',
        list(indicators.keys()),
        index=1
    )
    
    # Year range
    year_range = st.slider(
        'Select Year Range',
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()),
        value=(1980, int(df['year'].max()))
    )

# Filter data
filtered_df = df[
    (df['countryname'].isin(selected_countries)) &
    (df['year'] >= year_range[0]) &
    (df['year'] <= year_range[1])
]

# Create scatter plot
fig1 = px.scatter(
    filtered_df,
    x=indicators[x_indicator],
    y=indicators[y_indicator],
    color='countryname',
    hover_data=['year'],
    title=f'{x_indicator} vs {y_indicator}',
    labels={
        indicators[x_indicator]: x_indicator,
        indicators[y_indicator]: y_indicator,
        'countryname': 'Country'
    }
)

fig1.update_layout(height=600)
st.plotly_chart(fig1, use_container_width=True)

# Calculate correlation matrix
st.subheader("Correlation Matrix")
correlation_vars = list(indicators.values())
correlation_names = list(indicators.keys())

# Calculate correlation for each country
tabs = st.tabs(["All Countries"] + selected_countries)

with tabs[0]:
    corr_matrix = filtered_df[correlation_vars].corr()
    
    fig2 = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=correlation_names,
        y=correlation_names,
        text=np.round(corr_matrix, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        hoverongaps=False,
        colorscale='RdBu'
    ))
    
    fig2.update_layout(
        title='Correlation Matrix - All Selected Countries',
        height=600
    )
    st.plotly_chart(fig2, use_container_width=True)

# Individual country correlations
for i, country in enumerate(selected_countries, 1):
    with tabs[i]:
        country_df = filtered_df[filtered_df['countryname'] == country]
        corr_matrix = country_df[correlation_vars].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=correlation_names,
            y=correlation_names,
            text=np.round(corr_matrix, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False,
            colorscale='RdBu'
        ))
        
        fig.update_layout(
            title=f'Correlation Matrix - {country}',
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

# Time series of selected indicators
st.subheader("Time Series Comparison")
fig3 = go.Figure()

for country in selected_countries:
    country_data = filtered_df[filtered_df['countryname'] == country]
    
    fig3.add_trace(go.Scatter(
        x=country_data['year'],
        y=country_data[indicators[x_indicator]],
        name=f'{country} - {x_indicator}',
        line=dict(dash='solid')
    ))
    
    fig3.add_trace(go.Scatter(
        x=country_data['year'],
        y=country_data[indicators[y_indicator]],
        name=f'{country} - {y_indicator}',
        line=dict(dash='dash')
    ))

fig3.update_layout(
    height=400,
    title='Time Series of Selected Indicators',
    xaxis_title='Year',
    yaxis_title='Value'
)
st.plotly_chart(fig3, use_container_width=True) 