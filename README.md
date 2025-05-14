# Project Title: Interactive Heatmap Visualizer

This application is a Flask-based web tool that visualizes geographical data from a CSV file as an interactive, client-side rendered heatmap using Deck.gl.

## Features

- Displays a dynamic heatmap generated directly in the browser from CSV data (Latitude, Longitude, Value).
- Interactive map (pan, zoom) via Deck.gl.
- User controls to adjust heatmap parameters in real-time:
    - Layer Opacity
    - Radius of point influence
    - Intensity of data points
    - Threshold for data visibility
- Color scales are configurable via JSON files (see `colors/colors.json`).
- Application settings (default UI values, file paths) are configurable via `config.json`.

## Project Structure

- `app.py`: Main Flask application, handles routing and serves data.
- `config.py`: Handles loading application configuration from `config.json`.
- `config.json`: JSON file for user-configurable application settings.
- `utils/`: Contains utility modules.
  - `color_utils.py`: Manages loading and minifying color schemes.
- `templates/`: Contains HTML templates.
  - `index.html`: Main HTML page with Deck.gl map and controls.
- `static/`: Intended for static assets like CSS or client-side JS (if not using CDN).
- `colors/`: Color scheme definitions.
  - `colors.json`: Main color scheme file.
  - `colors.min.json`: Minified version, regenerated when colors are loaded.
- `data/`: Contains input data files.
  - `data.csv`: The primary dataset.
- `requirements.txt`: Python dependencies.
- `README.md`: This file.

## Configuration

The application can be configured by modifying the `config.json` file in the project root. If this file does not exist or is invalid, default settings from `config.py` will be used.

Support for an optional `config.yaml` file is included in `config.py` but is not enabled by default. To enable it, you would need to modify the `config.py` script (e.g., by uncommenting the relevant sections and setting an enable flag).

Key configurable options (see `config.json` for a full list and default values):
- `INPUT_CSV_FILE`: Path to the input data.
- `DEFAULT_MAP_OPACITY`: Initial opacity for the heatmap layer.
- `INITIAL_HEATMAP_RADIUS`, `INITIAL_HEATMAP_INTENSITY`, `INITIAL_HEATMAP_THRESHOLD`: Default values for heatmap controls.

Example `config.json` structure:
```json
{
    "INPUT_CSV_FILE": "data/my_custom_data.csv",
    "DEFAULT_MAP_OPACITY": 0.8,
    "INITIAL_HEATMAP_RADIUS": 50
    // ... other settings
}
```
Only include the settings you wish to override. Others will use defaults.

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
4.  **Ensure you have a `data/data.csv` file** (or configure the path in `config.json`) with columns 'Latitude', 'Longitude', and 'Value'.
5.  **Ensure you have a `colors/colors.json` file** for the color scale.

## Running the Application

```bash
python app.py
```

Then open your browser and navigate to `http://127.0.0.1:5000/` (or the address shown in the terminal). 