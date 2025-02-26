import streamlit as st

st.set_page_config(
    page_title="My Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("My Dashboard")
    st.write("Welcome to my dashboard!")
    
    # Add a sample chart
    import numpy as np
    chart_data = np.random.randn(20, 3)
    st.line_chart(chart_data)
    
    # Add some interactive elements
    with st.sidebar:
        st.header("Settings")
        option = st.selectbox(
            'Select a visualization',
            ['Line Chart', 'Bar Chart', 'Scatter Plot']
        )
        
        number = st.slider('Select a number', 0, 100, 50)
        st.write(f'Selected number: {number}')

if __name__ == "__main__":
    main()