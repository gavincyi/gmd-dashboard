import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Country Analysis", layout="wide")

def load_data():
    df = pd.read_csv('GMD.csv')
    return df

st.title("🌍 Detailed Country Analysis")
st.write("Analyze multiple economic indicators for a single country")

# Load the data
df = load_data()

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    
    # Country selection
    available_countries = sorted(df['countryname'].unique())
    selected_country = st.selectbox(
        'Select Country',
        available_countries,
        index=available_countries.index('United States') if 'United States' in available_countries else 0
    )
    
    # Year range selection
    year_range = st.slider(
        'Select Year Range',
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()),
        value=(1980, int(df['year'].max()))
    )

# Filter data for selected country
country_data = df[
    (df['countryname'] == selected_country) &
    (df['year'] >= year_range[0]) &
    (df['year'] <= year_range[1])
]

# Create multiple charts
col1, col2 = st.columns(2)

with col1:
    # GDP and Growth
    fig1 = make_subplots(rows=2, cols=1, subplot_titles=('Real GDP Growth', 'GDP Components (% of GDP)'))
    
    # Real GDP
    fig1.add_trace(
        go.Scatter(x=country_data['year'], y=country_data['rGDP'], name='Real GDP'),
        row=1, col=1
    )
    
    # GDP Components
    for component, color in [('cons_GDP', 'blue'), ('inv_GDP', 'green'), ('exports_GDP', 'red'), ('imports_GDP', 'orange')]:
        fig1.add_trace(
            go.Scatter(x=country_data['year'], y=country_data[component], 
                      name=component.replace('_GDP', '').title()),
            row=2, col=1
        )
    
    fig1.update_layout(height=600, showlegend=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Monetary and Price Indicators
    fig2 = make_subplots(rows=2, cols=1, subplot_titles=('Interest Rates', 'Inflation and Exchange Rate'))
    
    # Interest Rates
    for rate, name in [('strate', 'Short-term'), ('ltrate', 'Long-term'), ('cbrate', 'Central Bank')]:
        fig2.add_trace(
            go.Scatter(x=country_data['year'], y=country_data[rate], name=f'{name} Rate'),
            row=1, col=1
        )
    
    # Inflation and Exchange Rate
    fig2.add_trace(
        go.Scatter(x=country_data['year'], y=country_data['infl'], name='Inflation'),
        row=2, col=1
    )
    fig2.add_trace(
        go.Scatter(x=country_data['year'], y=country_data['REER'], name='REER'),
        row=2, col=1, yaxis='y2'
    )
    
    fig2.update_layout(height=600, showlegend=True)
    st.plotly_chart(fig2, use_container_width=True)

# Government Finances
st.subheader("Government Finances")
fig3 = go.Figure()

# Revenue and Expenditure
fig3.add_trace(go.Scatter(x=country_data['year'], y=country_data['govrev_GDP'], 
                         name='Revenue (% of GDP)', line=dict(color='green')))
fig3.add_trace(go.Scatter(x=country_data['year'], y=country_data['govexp_GDP'], 
                         name='Expenditure (% of GDP)', line=dict(color='red')))
fig3.add_trace(go.Scatter(x=country_data['year'], y=country_data['govdebt_GDP'], 
                         name='Debt (% of GDP)', line=dict(color='orange')))

fig3.update_layout(height=400, showlegend=True)
st.plotly_chart(fig3, use_container_width=True)

# Crisis Indicators
st.subheader("Crisis Periods")
crisis_data = country_data[['year', 'SovDebtCrisis', 'CurrencyCrisis', 'BankingCrisis']].melt(
    id_vars=['year'], 
    var_name='Crisis Type', 
    value_name='Crisis'
)
fig4 = px.scatter(crisis_data[crisis_data['Crisis'] == 1], 
                 x='year', y='Crisis Type', 
                 title='Crisis Events')
fig4.update_traces(marker=dict(size=10))
fig4.update_layout(height=200)
st.plotly_chart(fig4, use_container_width=True) 