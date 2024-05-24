# First Streamlit App!!
import streamlit as st
import pandas as pd
import numpy as np

# function to create a sample data frame and display it
def first_app():
    st.write("# Summer 2024 DoC with Streamlit")
    st.write("Here's our first attempt at using a dataframe to create a table:")
    st.write(pd.DataFrame({
        'variable01': [1, 2, 3, 4],
        'variable02': [10, 20, 30, 40]
    }))

    # Generate some sample data with numpy and display it
    another_dataset = np.random.randn(10, 20)
    st.dataframe(another_dataset)


# Call the first_app() function
first_app()