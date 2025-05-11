from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

df = pd.read_csv('netflix_data.csv')

def plot_content_type(filtered_df):
    data = filtered_df['type'].value_counts().reset_index()
    data.columns = ['type', 'count']
    fig = px.bar(data, x='type', y='count',
                 labels={'type': 'Type', 'count': 'Count'},
                 title='Distribution of Content Types',
                 color='type')
    return pio.to_html(fig, full_html=False)

def plot_top_countries(filtered_df):
    top_countries = filtered_df['country'].value_counts().head(10).reset_index()
    top_countries.columns = ['country', 'count']
    fig = px.bar(top_countries, x='country', y='count',
                 labels={'country': 'Country', 'count': 'Count'},
                 title='Top 10 Countries by Content',
                 color='country')
    return pio.to_html(fig, full_html=False)

def plot_release_years(filtered_df):
    years = filtered_df['release_year'].value_counts().sort_index().reset_index()
    years.columns = ['year', 'count']
    fig = px.line(years, x='year', y='count',
                  labels={'year': 'Year', 'count': 'Number of Releases'},
                  title='Content Releases Over Time')
    return pio.to_html(fig, full_html=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    selected_col = None

    # Dropdown options
    type_options = sorted(df['type'].dropna().unique())
    year_options = sorted(df['release_year'].dropna().unique())
    country_options = sorted(df['country'].dropna().unique())

    # Get selected filters from form or set defaults
    selected_type = request.form.get('type') or ''
    selected_year = request.form.get('release_year') or ''
    selected_country = request.form.get('country') or ''

    # Filter DataFrame
    filtered_df = df.copy()
    if selected_type:
        filtered_df = filtered_df[filtered_df['type'] == selected_type]
    if selected_year:
        filtered_df = filtered_df[filtered_df['release_year'] == int(selected_year)]
    if selected_country:
        filtered_df = filtered_df[filtered_df['country'] == selected_country]

    if request.method == 'POST':
        col = request.form.get('column')
        if col and col in df.columns:
            summary = filtered_df[col].describe().to_frame().to_html(classes="table table-striped")
            selected_col = col

    # Generate graphs with filtered data
    graph1 = plot_content_type(filtered_df)
    graph2 = plot_top_countries(filtered_df)
    graph3 = plot_release_years(filtered_df)
    return render_template(
        'index.html',
        columns=df.columns,
        summary=summary,
        selected_col=selected_col,
        graph1=graph1,
        graph2=graph2,
        graph3=graph3,
        type_options=type_options,
        year_options=year_options,
        country_options=country_options,
        selected_type=selected_type,
        selected_year=selected_year,
        selected_country=selected_country
    )

if __name__ == '__main__':
    app.run(debug=True)