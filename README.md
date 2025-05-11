# Netflix EDA Dashboard

This project is an interactive Flask web application for Exploratory Data Analysis (EDA) of Netflix titles. Users can filter the dataset by type, release year, and country, and view dynamic insights and summary statistics.

## Features

- Filter Netflix data by type, release year, and country
- View dynamic Plotly charts:
  - Distribution of Content Types
  - Top 10 Countries by Content
  - Content Releases Over Time
- View summary statistics for any column

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd "Netflix EDA"
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare the data

Place your `netflix_data.csv` file in the project directory.

### 4. Run the app

```bash
python app.py
```

Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## File Structure

- `app.py` - Main Flask application
- `templates/index.html` - HTML template for the dashboard
- `netflix_data.csv` - Netflix dataset (not included)
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Requirements

See `requirements.txt` for the full list.

## License

MIT License
