import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('netflix_data.csv')

st.set_page_config(page_title="Netflix EDA Dashboard", layout="centered")
st.title("🍿 Netflix EDA Dashboard")

# Add help/documentation
with st.expander("ℹ️ How to use this dashboard", expanded=False):
    st.markdown("""
    - **Filter** the data using the sidebar.
    - **Select X and Y columns** to visualize relationships.
    - **Choose a relationship type** for different graph styles.
    - **Summary statistics** for any column are shown on the right.
    - If no graph appears, check your selections or filters.
    """)

# Sidebar filters
st.sidebar.header("Filter Data")
type_options = sorted(df['type'].dropna().unique())
year_options = sorted(df['release_year'].dropna().unique())
country_options = sorted(df['country'].dropna().unique())
columns = df.columns.tolist()

selected_type = st.sidebar.selectbox("Type", options=["All"] + type_options)
selected_year = st.sidebar.selectbox("Year", options=["All"] + [str(y) for y in year_options])
selected_country = st.sidebar.selectbox("Country", options=["All"] + country_options)

# Filter DataFrame
filtered_df = df.copy()
if selected_type != "All":
    filtered_df = filtered_df[filtered_df['type'] == selected_type]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df['release_year'] == int(selected_year)]
if selected_country != "All":
    filtered_df = filtered_df[filtered_df['country'] == selected_country]

# Handle empty DataFrame
if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your filters.")
    st.stop()

st.markdown("### Custom Graph Generator")

relationship_type = st.radio(
    "Select Relationship Type",
    options=["Auto", "One-to-One", "One-to-Many", "Many-to-Many"],
    horizontal=True
)

col1, col2, col3 = st.columns(3)
with col1:
    selected_x = st.selectbox("X Column", options=["Select..."] + columns)
with col2:
    selected_y = st.selectbox("Y Column", options=["Select..."] + columns)
with col3:
    selected_col = st.selectbox("Summary Column", options=columns)

# Show summary statistics
if selected_col:
    st.markdown(f"#### Summary Statistics for `{selected_col}`")
    st.dataframe(filtered_df[selected_col].describe().to_frame())

# Input validation and user guidance
if (selected_x == "Select..." or selected_y == "Select..."):
    st.info("Please select both X and Y columns to generate a graph.")
else:
    x_dtype = df[selected_x].dtype
    y_dtype = df[selected_y].dtype

    # Warn if columns are not suitable for the selected relationship type
    warning = None
    if relationship_type in ["Auto", "One-to-One"]:
        if not (pd.api.types.is_numeric_dtype(x_dtype) and pd.api.types.is_numeric_dtype(y_dtype)):
            warning = "Scatter plots work best with numeric columns for both X and Y."
    elif relationship_type == "One-to-Many":
        if not pd.api.types.is_numeric_dtype(y_dtype):
            warning = "Bar plots work best when Y is numeric."
    elif relationship_type == "Many-to-Many":
        if pd.api.types.is_numeric_dtype(x_dtype) or pd.api.types.is_numeric_dtype(y_dtype):
            warning = "Heatmaps work best when both X and Y are categorical."

    if warning:
        st.warning(warning)

    # Graph customization: color by type (optional)
    color_by = st.selectbox("Color By (optional)", options=["None"] + columns, index=0)

    # Relationship-based graph selection
    fig = None
    if relationship_type == "Auto":
        if pd.api.types.is_numeric_dtype(x_dtype) and pd.api.types.is_numeric_dtype(y_dtype):
            fig = px.scatter(filtered_df, x=selected_x, y=selected_y, color=None if color_by == "None" else color_by,
                             title=f"{selected_y} vs {selected_x} (Scatter)")
        elif pd.api.types.is_numeric_dtype(y_dtype):
            fig = px.bar(filtered_df, x=selected_x, y=selected_y, color=None if color_by == "None" else color_by,
                         title=f"{selected_y} by {selected_x} (Bar)")
        else:
            fig = px.histogram(filtered_df, x=selected_x, color=None if color_by == "None" else color_by,
                               title=f"Distribution of {selected_x} (Histogram)")
    elif relationship_type == "One-to-One":
        fig = px.scatter(filtered_df, x=selected_x, y=selected_y, color=None if color_by == "None" else color_by,
                         title=f"One-to-One: {selected_y} vs {selected_x}")
    elif relationship_type == "One-to-Many":
        fig = px.bar(filtered_df, x=selected_x, y=selected_y, color=None if color_by == "None" else color_by,
                     title=f"One-to-Many: {selected_y} by {selected_x}")
    elif relationship_type == "Many-to-Many":
        if not (pd.api.types.is_numeric_dtype(x_dtype) or pd.api.types.is_numeric_dtype(y_dtype)):
            pivot = pd.pivot_table(filtered_df, index=selected_x, columns=selected_y, aggfunc='size', fill_value=0)
            fig = px.imshow(pivot, title=f"Many-to-Many: {selected_x} vs {selected_y} (Heatmap)")
        else:
            st.warning("Many-to-Many heatmap requires both X and Y to be categorical columns.")

    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)