# Netflix EDA Dashboard

This project is an interactive **Streamlit** web application for Exploratory Data Analysis (EDA) of Netflix titles. Users can filter the dataset by type, release year, and country, select columns for custom graphs, and view summary statistics.

## Features

- Filter Netflix data by type, release year, and country
- Select X and Y columns for custom graph generation
- Choose relationship type: Auto, One-to-One, One-to-Many, Many-to-Many
- View dynamic Plotly charts (scatter, bar, histogram, heatmap)
- View summary statistics for any column
- Optional color-by for graph customization
- User guidance and warnings for invalid selections

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AbdullahSaif-code/Netflix_EDA_Flask_app
cd Netflix_EDA_Flask_app
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare the data

Place your `netflix_data.csv` file in the project directory.

### 4. Run the app

```bash
streamlit run app.py
```

Open your browser and go to the local Streamlit URL shown in the terminal.

## File Structure

- `app.py` - Main Streamlit application
- `netflix_data.csv` - Netflix dataset (not included)
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Requirements

See `requirements.txt` for the full list.

## License

MIT License
