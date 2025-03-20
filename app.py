import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Global Macro Database Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_data():
    df = pd.read_csv('GMD.csv')
    return df

def main():
    st.title("Global Macro Database Dashboard")
    st.write("Compare economic indicators across countries")
    
    # Load the data
    df = load_data()
    
    # Sidebar controls
    with st.sidebar:
        st.header("Settings")
        
        # Country selection
        available_countries = sorted(df['countryname'].unique())
        default_countries = ['United States', 'China']
        selected_countries = st.multiselect(
            'Select Countries',
            available_countries,
            default=default_countries
        )
        
        # Indicator selection
        indicators = {
            # GDP and Growth
            'Real GDP (USD)': 'rGDP_USD',
            'Real GDP': 'rGDP',
            'Nominal GDP': 'nGDP',
            'Real GDP per capita': 'rGDP_pc',
            'GDP Deflator': 'deflator',
            
            # Consumption and Investment
            'Consumption': 'cons',
            'Real Consumption': 'rcons',
            'Consumption (% of GDP)': 'cons_GDP',
            'Investment': 'inv',
            'Investment (% of GDP)': 'inv_GDP',
            'Fixed Investment': 'finv',
            'Fixed Investment (% of GDP)': 'finv_GDP',
            
            # Trade
            'Exports': 'exports',
            'Exports (% of GDP)': 'exports_GDP',
            'Imports': 'imports',
            'Imports (% of GDP)': 'imports_GDP',
            'Current Account': 'CA',
            'Current Account (% of GDP)': 'CA_GDP',
            'USD Exchange Rate': 'USDfx',
            'Real Effective Exchange Rate': 'REER',
            
            # Government
            'Government Expenditure': 'govexp',
            'Government Expenditure (% of GDP)': 'govexp_GDP',
            'Government Revenue': 'govrev',
            'Government Revenue (% of GDP)': 'govrev_GDP',
            'Government Tax Revenue': 'govtax',
            'Government Tax Revenue (% of GDP)': 'govtax_GDP',
            'Government Deficit': 'govdef',
            'Government Deficit (% of GDP)': 'govdef_GDP',
            'Government Debt': 'govdebt',
            'Government Debt (% of GDP)': 'govdebt_GDP',
            
            # Prices and Population
            'House Price Index': 'HPI',
            'Consumer Price Index': 'CPI',
            'Inflation': 'infl',
            'Population': 'pop',
            'Unemployment Rate': 'unemp',
            
            # Interest Rates and Money Supply
            'Short-term Interest Rate': 'strate',
            'Long-term Interest Rate': 'ltrate',
            'Central Bank Rate': 'cbrate',
            'M0 Money Supply': 'M0',
            'M1 Money Supply': 'M1',
            'M2 Money Supply': 'M2',
            'M3 Money Supply': 'M3',
            'M4 Money Supply': 'M4',
            
            # Crisis Indicators
            'Sovereign Debt Crisis': 'SovDebtCrisis',
            'Currency Crisis': 'CurrencyCrisis',
            'Banking Crisis': 'BankingCrisis'
        }
        selected_indicator = st.selectbox(
            'Select Economic Indicator',
            list(indicators.keys())
        )
        
        # Year range selection
        year_range = st.slider(
            'Select Year Range',
            min_value=int(df['year'].min()),
            max_value=int(df['year'].max()),
            value=(1980, int(df['year'].max()))
        )
    
    # Filter data based on selections
    mask = (
        df['countryname'].isin(selected_countries) &
        (df['year'] >= year_range[0]) &
        (df['year'] <= year_range[1])
    )
    filtered_df = df[mask]
    
    # Create the plot
    if not filtered_df.empty:
        fig = px.line(
            filtered_df,
            x='year',
            y=indicators[selected_indicator],
            color='countryname',
            title=f'{selected_indicator} Comparison',
            labels={
                'year': 'Year',
                indicators[selected_indicator]: selected_indicator,
                'countryname': 'Country'
            }
        )
        
        # Update layout for better visualization
        fig.update_layout(
            height=600,
            hovermode='x unified',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show data table
        if st.checkbox('Show Raw Data'):
            st.dataframe(
                filtered_df[['countryname', 'year', indicators[selected_indicator]]]
                .sort_values(['countryname', 'year'])
            )
    else:
        st.warning('No data available for the selected countries and years.')

if __name__ == "__main__":
    main()