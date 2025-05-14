# Project Title: Interactive Heatmap Visualizer

This application is a Flask-based web tool that visualizes geographical data from a CSV file as an interactive heatmap overlay on a map. Users can inspect data points and dynamically adjust rendering parameters for a preview heatmap.

## Features

- Displays a high-resolution heatmap generated from CSV data (Latitude, Longitude, Value).
- Interactive map (pan, zoom).
- Point Inspector: Click on the map to get the interpolated data value at that coordinate.
- Dynamic Preview: Adjust parameters like color thresholds, resolution, DPI, and interpolation method to see a low-resolution preview update in real-time.
- Option to apply preview settings to regenerate the main high-resolution heatmap.
- Color scales are configurable via JSON files.

## Project Structure

- `app.py`: Main Flask application, handles routing and backend logic.
- `config.py`: Application configuration (file paths, raster settings, etc.).
- `utils/`: Contains utility modules.
  - `color_utils.py`: Manages loading and minifying color schemes.
  - `raster_utils.py`: (Presumed) Contains functions for raster generation and value interpolation.
- `static/`: Frontend assets.
  - `index.html`: Main HTML page with Leaflet/Deck.gl map and controls.
  - (Other CSS/JS if any)
- `colors/`: Color scheme definitions.
  - `colors.json`: Main color scheme file.
  - `colors.min.json`: Minified version, regenerated on startup.
- `data/`: Contains input data files.
  - `data.csv`: The primary dataset.
- `requirements.txt`: Python dependencies.
- `README.md`: This file.

## Setup

1.  **Clone the repository (if applicable).**
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Ensure you have a `data/data.csv` file** with columns 'Latitude', 'Longitude', and 'Value'.
5.  **Ensure you have a `colors/colors.json` file** for the color scale.

## Running the Application

```bash
python app.py
```

Then open your browser and navigate to `http://127.0.0.1:5000/` (or the address shown in the terminal). 