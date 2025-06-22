# Interactive Heatmap Visualizer

A modern Flask-based web application that creates interactive, real-time heatmap visualizations from CSV data using Deck.gl. Built with a **modular blueprint architecture** and **minimal friction integration**.

**Everything else is automatic!**

## Features

### Core Functionality
- **Real-time Interactive Heatmaps**: Dynamic heatmap rendering directly in the browser using Deck.gl
- **Integrated Sound Propagation**: Unified interface with heatmap and propagation simulation in one view
- **Multiple Dataset Support**: Load and switch between multiple CSV files with dropdown selector
- **Live Parameter Controls**: Adjust heatmap properties in real-time without page reloads:
  - Layer opacity slider
  - Point radius control
  - Intensity adjustment
  - Threshold filtering
- **Zero-Friction Blueprint Integration**: Copy files, import, and register - done
- **Smart CSV Handling**: Works with any CSV format automatically
- **Auto-Path Detection**: Finds its own resources without manual configuration

### User Interface
- **Unified Dashboard**: Single interface combining heatmap and sound propagation
- **Dataset Selector**: Dropdown menu for switching between multiple CSV files
- **Interactive Controls**: Intuitive sliders and toggles for all parameters
- **Propagation Timeline**: Integrated play/pause controls and keyboard shortcuts
- **Real-time Feedback**: Instant visual updates as parameters change
- **Collapsible Control Panel**: Hideable controls for maximum map viewing area
- **Enhanced Tooltips**: Detailed information on hover with formatted data display
- **Responsive Layout**: Works seamlessly on desktop and mobile devices
- **Modern Glassmorphism Design**: Professional UI with smooth animations

### Technical Features
- **Automatic Resource Detection**: Finds colors/, static/, templates/ directories automatically
- **Intelligent CSV Reading**: Handles files with/without index columns, multiple encodings
- **Smart Error Handling**: Helpful messages with file previews and suggestions
- **Multiple Heatmap Instances**: Support for multiple instances in a single application
- **Unified Configuration System**: Global defaults with per-instance overrides
- **High Performance**: Client-side rendering with WebGL acceleration via Deck.gl
- **Blueprint Architecture**: Seamless integration with existing Flask applications
- **Debug Endpoints**: Built-in troubleshooting and configuration info
- **API Endpoints**: RESTful API for data access and configuration

## Project Structure

```
├── app.py                      # Main Flask application with blueprint registration
├── heatmap_blueprint.py        # Modular blueprint with auto-detection
├── config.py                   # Configuration management and AppConfig class
├── config.json                 # User-configurable application settings
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation
├── INTEGRATION_README.md       # Blueprint integration guide
├── .gitignore                  # Git ignore patterns
├── templates/
│   └── map.html               # Unified dashboard (heatmap + propagation)
├── static/
│   └── *.png                  # Generated raster images and previews
├── utils/
│   └── color_utils.py         # Color scheme loading and management
├── colors/
│   ├── colors.json            # Color scale definitions (auto-detected)
│   └── colors.min.json        # Minified color schemes (auto-generated)
├── data/
│   ├── data.csv               # Primary dataset
│   ├── data2.csv              # Secondary dataset
│   └── data3.csv              # Tertiary dataset
├── examples/                   # Integration examples and tutorials
│   ├── simple_integration.py  # Basic single-file integration
│   ├── minimal_friction_example.py # Demonstrates zero-friction setup
│   ├── multiple_csv_dropdown.py # Multiple dataset example
│   ├── advanced_configuration.py # Multi-instance configuration
│   ├── flask_app_integration_example.py # Full integration example
│   └── README.md              # Examples documentation
└── venv/                      # Python virtual environment
```

## Quick Start

### For New Projects

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**
   ```bash
   python app.py
   ```

3. **Open your browser**
   Navigate to `http://127.0.0.1:5000/`

### For Integration into Existing Flask Apps

```python
from flask import Flask
from heatmap_blueprint import register_heatmap

app = Flask(__name__)

# Your existing routes here...

register_heatmap(app, INPUT_CSV_FILE='your_data.csv')

# OR with multiple CSV files:
csv_files = {
    'Dataset 1': 'data/data1.csv',
    'Dataset 2': 'data/data2.csv',
    'Dataset 3': 'data/data3.csv'
}

register_heatmap(app, CSV_FILES=csv_files)

app.run(debug=True)
```

**Automatic Features:**
- Auto-detects colors, static, and templates directories
- Smart CSV reading handles any CSV format automatically  
- No manual path configuration needed
- Intelligent error handling with helpful messages
- Resource fallbacks when files are missing
- Debug endpoints for troubleshooting

## Configuration

The application uses a **unified configuration system** with **automatic defaults**:

### Configuration Priority (highest to lowest):
1. **Runtime parameters** in `register_heatmap()`
2. **Global config.json** defaults
3. **Automatic smart defaults** (failsafe)

### Global Configuration (Optional)

Edit `config.json` to set global defaults for all heatmap instances:

```json
{
    "INPUT_CSV_FILE": "data/data.csv",
    "DEFAULT_MAP_OPACITY": 0.75,
    "INITIAL_HEATMAP_RADIUS": 40,
    "INITIAL_HEATMAP_INTENSITY": 1.5,
    "INITIAL_HEATMAP_THRESHOLD": 0.00,
    "STATIC_FOLDER": "static",
    "REQUIRED_COLUMNS": ["Latitude", "Longitude", "Value"]
}
```

### Runtime Configuration (Highest Priority)

Override defaults for specific heatmap instances:

```python
register_heatmap(app,
    CSV_FILES={
        'Survey A': 'data/survey_a.csv',
        'Survey B': 'data/survey_b.csv'
    },
    DEFAULT_CSV='Survey A',
    INITIAL_HEATMAP_RADIUS=60,      # Override global default
    INITIAL_HEATMAP_INTENSITY=2.0,  # Override global default
    URL_PREFIX='/custom-heatmap',
    BLUEPRINT_NAME='custom_heatmap'
)
```

### Configuration Parameters

#### Data Configuration
- **INPUT_CSV_FILE**: Path to single CSV data file (backward compatibility)
- **CSV_FILES**: Multiple datasets (dict format: `{'Display Name': 'file_path'}` or list format)
- **DEFAULT_CSV**: Which dataset to show by default (display name or filename)
- **REQUIRED_COLUMNS**: Expected column names in CSV files
- **COLORS_DIR**: Directory containing color scheme definitions (auto-detected)

#### Visualization Parameters
- **DEFAULT_MAP_OPACITY**: Initial opacity for the heatmap layer (0.0-1.0)
- **INITIAL_HEATMAP_RADIUS**: Default radius for heatmap points
- **INITIAL_HEATMAP_INTENSITY**: Default intensity multiplier
- **INITIAL_HEATMAP_THRESHOLD**: Minimum value threshold for display

#### Blueprint Configuration (All Auto-Detected)
- **URL_PREFIX**: Blueprint URL prefix (runtime only)
- **BLUEPRINT_NAME**: Internal blueprint name (runtime only, must be unique)
- **STATIC_FOLDER**: Static files directory (auto-detected)
- **TEMPLATE_FOLDER**: Templates directory (auto-detected)

## Data Format (Flexible)

Your CSV file can be in any format - the blueprint handles it automatically:

### Standard Format
```csv
Latitude,Longitude,Value
40.7128,-74.0060,25.3
40.7589,-73.9851,18.7
40.6892,-74.0445,31.2
```

### With Index Column
```csv
,Latitude,Longitude,Value
0,40.7128,-74.0060,25.3
1,40.7589,-73.9851,18.7
2,40.6892,-74.0445,31.2
```

### Any Encoding
- UTF-8, Latin-1, CP1252 automatically detected
- No more encoding errors

**Required columns:**
- **Latitude**: Geographic latitude coordinates
- **Longitude**: Geographic longitude coordinates  
- **Value**: Numeric values to visualize in the heatmap

## Multiple Dataset Support

### Dictionary Format (Recommended)
```python
csv_files = {
    'Airgun Survey 2023': 'data/airgun_2023.csv',
    'Airgun Survey 2022': 'data/airgun_2022.csv',
    'Baseline Noise': 'data/baseline.csv'
}

register_heatmap(app,
    CSV_FILES=csv_files,
    DEFAULT_CSV='Airgun Survey 2023'
)
```

### List Format (Auto-generated names)
```python
csv_files = [
    'data/survey_2023.csv',
    'data/survey_2022.csv',
    'data/baseline.csv'
]

register_heatmap(app,
    CSV_FILES=csv_files,
    DEFAULT_CSV='survey_2023'  # filename without extension
)
```

### UI Features
- **Dropdown Selector**: Switch between datasets in real-time
- **Dataset Information**: Current dataset name and file path displayed
- **Real-time Updates**: Map automatically updates when switching datasets
- **Error Handling**: Graceful handling of missing or invalid CSV files

## Sound Propagation Simulation

The application includes a sophisticated sound propagation visualization that demonstrates how sound waves travel through areas with varying noise resistance. **This functionality is integrated directly into the main heatmap view.**

### Interactive Controls

- **Play/Pause Button**: Start or stop the animation
- **Reset Button**: Return to the beginning of the simulation
- **Timeline Slider**: Scrub through any point in the 10-second animation
- **Dataset Selector**: Switch between different datasets for propagation analysis
- **Keyboard Shortcuts**:
  - `Space`: Play/pause animation
  - `←/→`: Step backward/forward one frame
  - `R`: Reset to beginning

### Technical Details

- **100 time steps** over a 10-second simulation
- **Physics-based calculation** considering distance and noise resistance
- **Real-time rendering** with WebGL acceleration
- **Optimized data processing** for smooth animation performance
- **Multi-dataset support** for comparative analysis

## Integration Examples

The `examples/` directory contains comprehensive integration examples:

### 1. Minimal Friction (`minimal_friction_example.py`)
Demonstrates the new zero-friction setup with automatic configuration.

### 2. Simple Integration (`simple_integration.py`)
Basic blueprint integration with minimal configuration.

### 3. Multiple CSV Dropdown (`multiple_csv_dropdown.py`)
Demonstrates the dropdown selector functionality with multiple datasets.

### 4. Advanced Configuration (`advanced_configuration.py`)
Multiple heatmap instances with different configurations in a single application.

### 5. Flask App Integration (`flask_app_integration_example.py`)
Complete example of integrating into an existing Flask application.

See [`INTEGRATION_README.md`](INTEGRATION_README.md) for detailed integration guide.

## API Endpoints

### Main Routes
- **GET /**: Redirects to heatmap dashboard
- **GET /{URL_PREFIX}/**: Unified dashboard with heatmap and propagation visualization

### Data API
- **GET /{URL_PREFIX}/data**: Returns default CSV data as JSON
- **GET /{URL_PREFIX}/data/{csv_key}**: Returns specific dataset as JSON
- **GET /{URL_PREFIX}/csv-files**: Returns list of available CSV files

### Debug & Configuration
- **GET /{URL_PREFIX}/config-info**: Returns configuration information and auto-detected paths
- **GET /{URL_PREFIX}/test-data**: Tests CSV loading and shows file structure

### Static Assets
- **GET /{URL_PREFIX}/static/{filename}**: Serves static assets (auto-detected)

## Dependencies

Key Python packages:
- **Flask**: Web framework and blueprint system
- **pandas**: Data manipulation and CSV processing
- **numpy**: Numerical computations for propagation simulation
- **Flask-CORS**: Cross-origin resource sharing
- **Flask-Compress**: Response compression

Frontend libraries (CDN):
- **Deck.gl**: WebGL-powered data visualization
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide Icons**: Modern icon library

## Browser Compatibility

- Chrome/Chromium 60+
- Firefox 55+
- Safari 12+
- Edge 79+

WebGL support is required for optimal performance.

## Performance Notes

- The application renders heatmaps client-side using WebGL for optimal performance
- Large datasets (>100k points) may require parameter tuning for smooth interaction
- Color schemes are minified automatically for faster loading
- Multiple datasets are loaded on-demand to reduce initial load time
- Blueprint architecture allows for multiple independent heatmap instances
- Auto-detection minimizes startup overhead

## Troubleshooting

### Built-in Debug Tools

#### Configuration Info
Access debug information at: `http://your-app/heatmap/config-info`

Shows:
- Configuration sources and values
- Auto-detected paths
- CSV file status
- Error details

#### CSV Testing
Test your CSV files at: `http://your-app/heatmap/test-data`

Shows:
- CSV file structure
- Column detection
- Sample data
- Loading errors with suggestions

### Common Issues (Now Auto-Fixed)

1. **CSV file format** - Auto-handled with smart reading
2. **Missing resource directories** - Auto-detected with fallbacks 
3. **Path configuration** - Auto-configured relative to blueprint
4. **Encoding issues** - Auto-detected (utf-8, latin-1, cp1252)
5. **Index column problems** - Handles with/without index automatically

### Remaining Issues

1. **CSV file not found**: Ensure your data files exist in the specified paths
2. **Missing required columns**: Verify your CSV has Latitude, Longitude, and Value columns
3. **Performance issues**: Try reducing the radius or intensity for large datasets
4. **Browser compatibility**: Ensure WebGL is enabled in your browser
5. **Blueprint conflicts**: Use unique `BLUEPRINT_NAME` for multiple instances

### Smart Error Messages

The blueprint now provides detailed error messages with:
- File preview for CSV issues
- Path information for missing resources
- Suggestions for fixing problems
- Auto-detected alternatives

## Development and Customization

### Adding New Features

The blueprint architecture makes it easy to extend functionality:

1. **Custom Routes**: Add new routes to the blueprint
2. **Configuration Options**: Extend the `HeatmapConfig` class
3. **Data Processing**: Modify data loading and processing functions
4. **UI Components**: Customize templates and static assets

### Color Schemes

Customize color schemes by editing `colors/colors.json` (auto-detected):

```json
[
  [0, "#80D6EA"],
  [0.5, "#F7DC6F"],
  [1, "#8B0000"]
]
```

### Templates

The application uses one main template:
- `templates/map.html`: Unified interface with heatmap and sound propagation

The template supports the full configuration system, multiple dataset functionality, and integrated propagation visualization.
