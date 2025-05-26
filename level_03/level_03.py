# Example that shows how to hit a REST API and display the data in 
# Streamlit. 

import streamlit as st
import pandas as pd
import requests
import altair as alt

# Base URL is a sample API we put online
# Docs at https://doc-api-nato-vmjes.ondigitalocean.app/docs
API_BASE_URL = "https://doc-api-nato-vmjes.ondigitalocean.app"

# Function to fetch data from the API
def fetch_nato_api_data(endpoint_path):
    """Fetches data from the given API endpoint path."""
    full_url = f"{API_BASE_URL}{endpoint_path}"
    try:
        response = requests.get(full_url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from {full_url}: {e}")
        return None
    except requests.exceptions.JSONDecodeError:
        st.error(f"Error decoding JSON from {full_url}. Response content: {response.text}")
        return None

def nato_data_explorer_app():
    st.set_page_config(layout="wide")
    st.title("NATO API Data Explorer")
    st.markdown(
        "This application fetches, displays, and visualizes data from the "
        "[NATO API](https://doc-api-nato-vmjes.ondigitalocean.app/docs) "
        "covering member countries and expenditures."
    )

    st.sidebar.header("Data Selection")
    data_option = st.sidebar.selectbox(
        "Choose data to explore:",
        ("Member Countries", "Defense Expenditures (% of GDP)")
    )

    if data_option == "Member Countries":
        endpoint = "/countries"
        data_key = "countries_data"
        data_name = "Countries"
    elif data_option == "Defense Expenditures (% of GDP)":
        endpoint = "/expenditures/gdp_pct"
        data_key = "expenditures_data"
        data_name = "Expenditures (% GDP)"
    else:
        return # Should not happen with selectbox

    if st.sidebar.button(f"Fetch {data_name}", key=f"fetch_{data_key}"):
        st.session_state[data_key] = None # Reset previous data
        with st.spinner(f"Fetching {data_name} from API..."):
            fetched_data = fetch_nato_api_data(endpoint)
            if fetched_data is not None:
                st.session_state[data_key] = fetched_data
                if not fetched_data:
                    st.warning(f"API returned no {data_name.lower()}.")
                else:
                    st.success(f"Successfully fetched {len(fetched_data)} records for {data_name.lower()}.")

    # Display fetched data and visualizations
    if data_key in st.session_state and st.session_state[data_key]:
        current_data = st.session_state[data_key]
        df = pd.DataFrame(current_data)

        st.header(f"{data_name} Data")

        with st.expander("Show Raw JSON Data (sample)", expanded=False):
            st.json(current_data[:min(3, len(current_data))])

        st.subheader("Tabular Data")
        st.dataframe(df, use_container_width=True)
        st.write("**Add Code here to visualize something from the data frame above.**")
        
        # --------    ADD YOUR CODE HERE    --------        

        
    else:
        st.info(f"Click the 'Fetch {data_name}' button in the sidebar to load and display data.")

# Run the app
if __name__ == "__main__":
    nato_data_explorer_app()