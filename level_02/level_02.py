# Sample Streamlit app showing some of its data Viz

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# import plotly.graph_objects as go 

def visualization_demo():

    st.title("Streamlit Data Visualization Demo")
    st.markdown("This application demos various data visualization " 
                "capabilities within Streamlit, including native "
                " charts and integrations with libraries like Plotly.")

    # ------ Sample Data Generation ------
    st.header("Sample Data")
    st.write("We are going to use randomly generated data for these examples.")

    # Sample Data for line, area, and bar charts
    chart_data_options = {
        'Data Type A': np.random.randn(20, 3),
        'Data Type B': np.random.rand(20, 3) * 100,
        'Data Type C': np.abs(np.random.randn(20, 3))
    }
    selected_data_type = st.selectbox("Use this select box to choose the"  
                                      " data characteristics for some charts:", 
                                      list(chart_data_options.keys()))
    chart_data = pd.DataFrame(
        chart_data_options[selected_data_type],
        columns=['Series 1', 'Series 2', 'Series 3']
    )
    st.write("Sample data for line, area, and bar charts:")
    st.dataframe(chart_data.head())

    # Here is some random data for scatter plots and other Plotly charts
    scatter_data = pd.DataFrame(
        np.random.rand(100, 4) * np.array([100, 1000, 10, 5]),
        columns=['X Value', 'Y Value', 'Size', 'Category']
    )
    scatter_data['Category'] = pd.Series(np.random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'], size=100)).astype('category')
    st.write("Sample data for scatter and other complex charts:")
    st.dataframe(scatter_data.head())

    # Data for usage with maps
    map_points = np.random.randn(200, 2) / np.array([30, 30]) + np.array([50.85, 4.35]) # Centered around Brussels
    map_data = pd.DataFrame(map_points, columns=['lat', 'lon'])
    map_data['size'] = np.random.rand(200) * 100 # Add size for potential use in st.pydeck_chart

    st.divider()

    # ------ 2: Streamlit Native Charts ------
    st.header("Streamlit Native Charts Demo")

    st.subheader("Line Chart")
    st.write("`st.line_chart` is good for displaying trends over time or ordered categories.")
    st.line_chart(chart_data)

    st.subheader("Area Chart")
    st.write("`st.area_chart` is like a line chart, but it fills the area below the line.")
    st.area_chart(chart_data)

    st.subheader("Bar Chart")
    st.write("`st.bar_chart` is used for comparing quantities across different categories.")
    st.bar_chart(chart_data)

    st.subheader("Streamlit's Native Scatter Chart")
    st.write("""`st.scatter_chart` provides a basic scatter plot. 
             For more customization, use `st.plotly_chart`.""")
    
    # st.scatter_chart often works better with specific x and y columns
    st_scatter_data = pd.DataFrame(np.random.randn(50, 2), columns=['x', 'y'])
    
    # Helper function to generate a random hex RGB color
    def random_hex_color():
        r = int(np.random.rand() * 255)
        g = int(np.random.rand() * 255)
        b = int(np.random.rand() * 255)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    # Generate random colors for each point
    st_scatter_data['color'] = [random_hex_color() for _ in range(50)]
    st_scatter_data['size'] = np.random.rand(50) * 1000
    st.scatter_chart(st_scatter_data, x='x', y='y', size='size', color='color')
    st.info("Important Note: `st.scatter_chart` expects color as a hex string column.")

    st.divider()
   
    # ------ 3: Plotly Express Integration ------
    st.header("Plotly Express Charts")
    st.write("Streamlit integrates with Plotly to give you more options for "
             "interactive charts.  Use `st.plotly_chart` to display Plotly figures.")

    st.subheader("Plotly Scatter Plot")
    st.write("More customizable scatter plots. You get " 
             "hover effects, color mapping, and size variations.")
    fig_scatter = px.scatter(
        scatter_data,
        x="X Value",
        y="Y Value",
        color="Category",
        size="Size",
        hover_name="Category",
        title="Interactive Scatter Plot (Plotly)",
        marginal_y="violin",
        marginal_x="box"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("Plotly Histogram")
    st.write("Visualizing the distribution of a single numerical variable.")
    fig_hist = px.histogram(
        scatter_data,
        x="Y Value",
        color="Category",
        nbins=30,
        title="Histogram of Y Values by Category (Plotly)",
        opacity=0.8,
        barmode='overlay' # or 'stack', 'group'
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    st.subheader("Plotly Box Plot")
    st.write("Displaying the distribution of data based on a five-number summary.")
    fig_box = px.box(
        scatter_data,
        x="Category",
        y="Y Value",
        color="Category",
        title="Box Plot of Y Values by Category (Plotly)",
        points="all" # "all", "outliers", "suspectedoutliers", or False
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("Plotly Pie Chart")
    pie_data_grouped = scatter_data.groupby("Category")['Size'].sum().reset_index()
    fig_pie = px.pie(
        pie_data_grouped,
        values='Size',
        names='Category',
        title='Pie Chart of Total Size by Category (Plotly)'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Customized Plotly Bar Chart")
    st.write("Plotly offers tons of customizations for bar charts.")
    bar_data_agg = scatter_data.groupby("Category")["X Value"].mean().reset_index()
    fig_bar_plotly = px.bar(
        bar_data_agg,
        x="Category",
        y="X Value",
        color="Category",
        title="Average X Value by Category (Plotly Bar)",
        text_auto=True # Display values on bars
    )
    fig_bar_plotly.update_layout(xaxis_title="Category Type", yaxis_title="Mean X Value")
    st.plotly_chart(fig_bar_plotly, use_container_width=True)

    # ------ 4: Maps ------
    st.header("Map Visualizations")

    st.subheader("Simple Map with `st.map`")
    st.write("`st.map` plots data points on a map using latitude and longitude.")
    st.map(map_data, size=10, zoom=6) # Added size and zoom

    st.subheader("Advanced Map with `st.pydeck_chart`")
    st.write("`st.pydeck_chart` offers more sophisticated map visualizations using DeckGL.")
    try:
        import pydeck as pdk
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=50.85,
                longitude=4.35,
                zoom=7,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                   'HexagonLayer',
                   data=map_data,
                   get_position='[lon, lat]',
                   radius=1000,
                   elevation_scale=40,
                   elevation_range=[0, 1000],
                   pickable=True,
                   extruded=True,
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=map_data,
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]', # R, G, B, Alpha
                    get_radius='size', # Use the 'size' column for radius
                    pickable=True
                )
            ],
            tooltip={"text": "Lat: {lat}, Lon: {lon}\nSize: {size}"}
        ))
    except ImportError:
        st.warning("Pydeck library not installed. Skipping `st.pydeck_chart`" 
                   " demo. Install with `pip install pydeck`.")


    st.divider()

    st.header("Other Plotting Libraries")
    st.write(
        "Streamlit also supports other popular plotting libraries like Matplotlib, Seaborn, Altair, Vega-Lite, and Bokeh. "
        "You typically generate a figure object using the library and then pass it to the appropriate Streamlit command "
        "(e.g., `st.pyplot()` for Matplotlib)."
    )
    st.write("For brevity, those are not demonstrated here but follow a similar pattern to the Plotly integration.")


# Call the visualization_demo() function
if __name__ == "__main__":
    visualization_demo()