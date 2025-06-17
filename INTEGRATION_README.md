# Heatmap Blueprint Integration Guide

This guide shows how to integrate your **Heatmap Airgun** project into existing Flask applications using Flask Blueprints.

## 🚀 Quick Start

### Simplest Integration (1 line of code!)

```python
from flask import Flask
from heatmap_blueprint import register_heatmap

app = Flask(__name__)

# Add your existing routes here
@app.route('/')
def home():
    return "My existing Flask app"

# Add heatmap functionality
register_heatmap(app)

if __name__ == '__main__':
    app.run(debug=True)
```

Your heatmap will now be available at:
- `http://localhost:5000/heatmap/` - Main heatmap view
- `http://localhost:5000/heatmap/propagation` - Sound propagation animation
- `http://localhost:5000/heatmap/data` - Data API endpoint
- `http://localhost:5000/heatmap/propagation-data` - Propagation simulation data

## 📁 Project Structure

```
your-existing-project/
├── app.py                    # Your existing Flask app
├── heatmap_blueprint.py      # The modular heatmap blueprint
├── integration_examples.py   # Usage examples
├── data/
│   └── data.csv             # Your CSV data file
├── templates/
│   ├── index.html           # Heatmap main view
│   └── propagation.html     # Propagation view
├── colors/
│   └── colors.json          # Color configuration
└── static/                  # Static assets (if any)
```

## ⚙️ Configuration Options

The blueprint accepts these configuration parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `INPUT_CSV_FILE` | `'data/data.csv'` | Path to your CSV data file (backward compatibility) |
| `CSV_FILES` | `None` | **NEW**: Dict or list of CSV files for multi-file support |
| `DEFAULT_CSV` | `None` | **NEW**: Default CSV file to display |
| `STATIC_FOLDER` | `'static'` | Static files directory |
| `TEMPLATE_FOLDER` | `'templates'` | Templates directory |
| `COLORS_DIR` | `'colors'` | Color configuration directory |
| `URL_PREFIX` | `'/heatmap'` | URL prefix for all routes |
| `BLUEPRINT_NAME` | `'heatmap'` | Blueprint name (must be unique) |
| `REQUIRED_COLUMNS` | `['Latitude', 'Longitude', 'Value']` | Required CSV columns |
| `DEFAULT_MAP_OPACITY` | `0.75` | Default heatmap opacity |
| `INITIAL_HEATMAP_RADIUS` | `40` | Initial heatmap point radius |
| `INITIAL_HEATMAP_INTENSITY` | `1.5` | Initial heatmap intensity |
| `INITIAL_HEATMAP_THRESHOLD` | `0.00` | Initial heatmap threshold |

## 🎯 Integration Examples

### 1. Multiple CSV Files (Dictionary Format)

```python
from heatmap_blueprint import register_heatmap

# Multiple CSV files with custom display names
csv_files = {
    'Airgun Survey 2023': 'data/airgun_2023.csv',
    'Airgun Survey 2022': 'data/airgun_2022.csv', 
    'Baseline Noise': 'data/baseline.csv'
}

register_heatmap(app,
    CSV_FILES=csv_files,
    DEFAULT_CSV='Airgun Survey 2023',
    URL_PREFIX='/noise-analysis',
    INITIAL_HEATMAP_RADIUS=60,
    INITIAL_HEATMAP_INTENSITY=2.0
)
```

### 2. Multiple CSV Files (List Format)

```python
# List of CSV files (display names auto-generated from filenames)
csv_files = [
    'data/survey_2023.csv',
    'data/survey_2022.csv', 
    'data/survey_2021.csv'
]

register_heatmap(app,
    CSV_FILES=csv_files,
    DEFAULT_CSV='survey_2023',  # filename without extension
    URL_PREFIX='/surveys'
)
```

### 3. Single CSV File (Backward Compatibility)

```python
register_heatmap(app, 
    INPUT_CSV_FILE='my_data/noise_data.csv',
    URL_PREFIX='/noise-analysis',
    INITIAL_HEATMAP_RADIUS=60,
    INITIAL_HEATMAP_INTENSITY=2.0
)
```

### 4. Multiple Heatmap Instances (Different Data Types)

```python
# Airgun survey data with multiple files
airgun_files = {
    'Zone A': 'data/airgun_zone_a.csv',
    'Zone B': 'data/airgun_zone_b.csv'
}

register_heatmap(app,
    CSV_FILES=airgun_files,
    URL_PREFIX='/airgun-analysis',
    BLUEPRINT_NAME='airgun_heatmap'
)

# Traffic noise data with multiple time periods
traffic_files = {
    'Peak Hours': 'data/traffic_peak.csv',
    'Off-Peak Hours': 'data/traffic_offpeak.csv'
}

register_heatmap(app,
    CSV_FILES=traffic_files,
    URL_PREFIX='/traffic-analysis',
    BLUEPRINT_NAME='traffic_heatmap',
    COLORS_DIR='colors/traffic'
)
```

### 3. Advanced Configuration with Class

```python
from heatmap_blueprint import HeatmapConfig, create_heatmap_blueprint

# Create custom configuration
config = HeatmapConfig(
    INPUT_CSV_FILE='environmental_data/measurements.csv',
    URL_PREFIX='/environmental-analysis',
    BLUEPRINT_NAME='env_monitoring',
    INITIAL_HEATMAP_RADIUS=45,
    DEFAULT_MAP_OPACITY=0.8
)

# Create and register blueprint
blueprint = create_heatmap_blueprint(config)
app.register_blueprint(blueprint)
```

### 4. Integration with Authentication

```python
from heatmap_blueprint import create_heatmap_blueprint

# Create blueprint
heatmap_bp = create_heatmap_blueprint()

# Add authentication to all routes
@heatmap_bp.before_request
def require_login():
    if not is_user_logged_in():
        return redirect(url_for('login'))

app.register_blueprint(heatmap_bp)
```

## 📊 Data Format Requirements

Your CSV file should have these columns:

```csv
,Latitude,Longitude,Value,Bathy,Sector
1,37.25897980148502,-59.3,88.04606789424417,"[1003, 5163.03076171875]",0.0
2,37.24995686563234,-59.3,88.04978137920247,"[2007, 5167.09033203125]",0.0
...
```

**Required columns:**
- `Latitude` - Geographic latitude
- `Longitude` - Geographic longitude  
- `Value` - The value to visualize (noise level, temperature, etc.)

**Optional columns:**
- Additional columns are ignored but can be present

## 🎨 Color Customization

Create a `colors.json` file in your colors directory:

```json
[
    [0.0, "#80D6EA"],
    [0.5, "#FFD700"], 
    [1.0, "#8B0000"]
]
```

Format: `[position, color]` where position is 0.0-1.0

## 🔧 Dependencies

Make sure these are in your `requirements.txt`:

```txt
Flask>=2.0.0
flask-cors>=3.0.0
flask-compress>=1.10.0
pandas>=1.3.0
numpy>=1.21.0
```

## 🛠️ API Endpoints

Once integrated, your app will have these new endpoints:

### `GET {URL_PREFIX}/`
Main heatmap visualization interface with CSV selector dropdown

### `GET {URL_PREFIX}/propagation`  
Sound propagation animation interface with CSV selector dropdown

### `GET {URL_PREFIX}/csv-files`
**NEW**: Returns list of available CSV files:
```json
{
    "files": {
        "Survey 2023": "data/survey_2023.csv",
        "Survey 2022": "data/survey_2022.csv"
    },
    "default": "Survey 2023"
}
```

### `GET {URL_PREFIX}/data` or `GET {URL_PREFIX}/data/<csv_key>`
Returns JSON with heatmap data for default or specific CSV:
```json
{
    "data": [
        {"Latitude": 37.259, "Longitude": -59.3, "Value": 88.046},
        ...
    ],
    "valueRange": {"min": 45.2, "max": 92.8},
    "colorScale": [[0, "#80D6EA"], [1, "#8B0000"]],
    "csvKey": "Survey 2023",
    "csvFile": "data/survey_2023.csv"
}
```

### `GET {URL_PREFIX}/propagation-data` or `GET {URL_PREFIX}/propagation-data/<csv_key>`
Returns JSON with animation frames for propagation simulation for specific CSV

### `GET {URL_PREFIX}/test-data` or `GET {URL_PREFIX}/test-data/<csv_key>`
Returns basic info about your dataset for debugging

## 🔍 Troubleshooting

### Common Issues

1. **Import Error**: Make sure `heatmap_blueprint.py` is in the same directory or in your Python path

2. **Template Not Found**: Ensure your `templates/` directory contains `index.html` and `propagation.html`

3. **Data Not Loading**: Check that your CSV file path is correct and has the required columns

4. **Color Issues**: Verify your `colors/colors.json` file exists and has valid color format

5. **Blueprint Name Conflicts**: If integrating multiple instances, ensure each has a unique `BLUEPRINT_NAME`

### Debug Mode

Enable debug information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

register_heatmap(app, INPUT_CSV_FILE='your_file.csv')
```

## 📝 Migration from Standalone App

If you have the original standalone app, here's how to migrate:

1. **Copy files**: Move `heatmap_blueprint.py` to your existing project
2. **Update imports**: Replace `from config import AppConfig` with blueprint configuration
3. **Update routes**: Change from `@app.route` to blueprint registration
4. **Test**: Use the `/test-data` endpoint to verify data loading

## 🎉 Examples

See `integration_examples.py` for complete working examples:

```bash
python integration_examples.py 1  # Simple integration
python integration_examples.py 2  # Custom config
python integration_examples.py 3  # Multiple heatmaps
python integration_examples.py 4  # Advanced usage
python integration_examples.py 5  # With authentication
```

## 📄 License

Same license as your original project.

## 🤝 Contributing

To add features to the blueprint:

1. Modify `heatmap_blueprint.py`
2. Add configuration options to `HeatmapConfig`
3. Update this README
4. Add examples to `integration_examples.py`

---

**Happy mapping!** 🗺️✨ 