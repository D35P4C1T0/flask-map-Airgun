# Heatmap Blueprint Integration Guide

## Overview

The Interactive Heatmap Visualizer is built as a **Flask blueprint** for seamless integration into existing Flask applications. This guide provides comprehensive instructions for integrating the heatmap functionality with minimal setup requirements.

## Quick Start Integration

**Basic integration (one line):**
```python
from flask import Flask
from heatmap_blueprint import register_heatmap

app = Flask(__name__)

# Your existing routes...

register_heatmap(app, INPUT_CSV_FILE='your_data.csv')

app.run(debug=True)
```

**Multi-dataset integration:**
```python
csv_files = {
    'Dataset A': 'data/dataset_a.csv',
    'Dataset B': 'data/dataset_b.csv',
    'Dataset C': 'data/dataset_c.csv'
}

register_heatmap(app, CSV_FILES=csv_files, DEFAULT_CSV='Dataset A')
```

### 4. Access Application

Navigate to `http://your-app/heatmap/` to access the visualization interface.

## Automatic Features

The blueprint includes intelligent auto-detection and configuration:

### Path Auto-Detection
- **Automatic discovery** of colors/, static/, and templates/ directories
- **Relative path resolution** from blueprint file location
- **Graceful fallbacks** when directories are missing
- **No manual path configuration** required

### Smart CSV Handling
- **Multiple encoding support**: UTF-8, Latin-1, CP1252
- **Flexible format support**: With or without index columns
- **Intelligent error messages** with file previews
- **Automatic format detection** and handling

### Error Handling
- **Detailed error messages** with specific file information
- **Debug endpoints** for troubleshooting
- **Configuration validation** with helpful suggestions
- **Resource fallback** mechanisms

## Integration Examples

### Minimal Friction Setup

```python
from flask import Flask
from heatmap_blueprint import register_heatmap

app = Flask(__name__)

# That's it - everything else is automatic
register_heatmap(app, INPUT_CSV_FILE='data.csv')

if __name__ == '__main__':
    app.run(debug=True)
```

### Multiple Instances

```python
from flask import Flask
from heatmap_blueprint import register_heatmap

app = Flask(__name__)

# Primary heatmap instance
register_heatmap(app,
    CSV_FILES={'Data 1': 'data/data1.csv'},
    URL_PREFIX='/map1',
    BLUEPRINT_NAME='data1_heatmap'
)

# Secondary heatmap instance
register_heatmap(app,
    CSV_FILES={'Data 2': 'data/data2.csv'},
    URL_PREFIX='/map2',
    BLUEPRINT_NAME='data2_heatmap'
)

app.run(debug=True)
```

### Advanced Configuration

```python
from flask import Flask
from heatmap_blueprint import register_heatmap

app = Flask(__name__)

register_heatmap(app,
    CSV_FILES={
        'Airgun Data': 'data/data1.csv',
        'Marine Traffic': 'data/data2.csv',
        'Baseline Noise': 'data/data3.csv'
    },
    DEFAULT_CSV='Airgun Data',
    INITIAL_HEATMAP_RADIUS=50,
    INITIAL_HEATMAP_INTENSITY=2.0,
    DEFAULT_MAP_OPACITY=0.8,
    URL_PREFIX='/marine-acoustics',
    BLUEPRINT_NAME='marine_heatmap'
)

app.run(debug=True)
```

## Configuration Parameters

### Runtime Configuration (Highest Priority)

Pass parameters directly to `register_heatmap()`:

```python
register_heatmap(app,
    # Data Configuration
    INPUT_CSV_FILE='data/single_file.csv',  # Single file (backward compatibility)
    CSV_FILES=csv_files_dict,               # Multiple files (recommended)
    DEFAULT_CSV='display_name',             # Default dataset
    
    # Visualization Parameters
    INITIAL_HEATMAP_RADIUS=40,              # Point radius
    INITIAL_HEATMAP_INTENSITY=1.5,          # Intensity multiplier
    DEFAULT_MAP_OPACITY=0.75,               # Layer opacity
    INITIAL_HEATMAP_THRESHOLD=0.1,          # Minimum value threshold
    
    # Blueprint Configuration
    URL_PREFIX='/custom-path',              # URL prefix for routes
    BLUEPRINT_NAME='unique_name',           # Internal blueprint name
    
    # Advanced Options
    REQUIRED_COLUMNS=['Lat', 'Lon', 'Val'], # Custom column names
    COLORS_DIR='custom/colors',             # Override auto-detection
    STATIC_FOLDER='custom/static',          # Override auto-detection
    TEMPLATE_FOLDER='custom/templates'      # Override auto-detection
)
```

### Global Configuration (Optional)

Create `config.json` for application-wide defaults:

```json
{
    "INPUT_CSV_FILE": "data/default.csv",
    "DEFAULT_MAP_OPACITY": 0.75,
    "INITIAL_HEATMAP_RADIUS": 40,
    "INITIAL_HEATMAP_INTENSITY": 1.5,
    "INITIAL_HEATMAP_THRESHOLD": 0.0,
    "REQUIRED_COLUMNS": ["Latitude", "Longitude", "Value"]
}
```

### Configuration Priority

1. **Runtime parameters** in `register_heatmap()` (highest)
2. **Global config.json** settings
3. **Automatic smart defaults** (lowest)

## CSV Data Format

### Supported Formats

The blueprint automatically handles multiple CSV formats:

#### Standard Format
```csv
Latitude,Longitude,Value
40.7128,-74.0060,25.3
40.7589,-73.9851,18.7
```

#### With Index Column
```csv
,Latitude,Longitude,Value
0,40.7128,-74.0060,25.3
1,40.7589,-73.9851,18.7
```

#### Custom Column Names
```csv
Lat,Lon,Sound_Level
40.7128,-74.0060,25.3
40.7589,-73.9851,18.7
```

### Multiple Dataset Configuration

#### Dictionary Format (Recommended)
```python
csv_files = {
    'Q1 2023 Survey': 'data/q1_2023.csv',
    'Q2 2023 Survey': 'data/q2_2023.csv',
    'Baseline Study': 'data/baseline.csv'
}
```

#### List Format (Auto-naming)
```python
csv_files = [
    'data/survey_2023.csv',
    'data/survey_2022.csv',
    'data/baseline.csv'
]
# Auto-generates display names: "survey_2023", "survey_2022", "baseline"
```

### Encoding Support

Automatic encoding detection handles:
- UTF-8 (default)
- Latin-1 (ISO-8859-1)
- CP1252 (Windows-1252)

## API Routes

Each blueprint instance provides these endpoints:

### Core Routes
- **GET /{URL_PREFIX}/**: Main visualization interface
- **GET /{URL_PREFIX}/data**: Default dataset as JSON
- **GET /{URL_PREFIX}/data/{csv_key}**: Specific dataset as JSON

### Configuration & Debug
- **GET /{URL_PREFIX}/csv-files**: Available datasets list
- **GET /{URL_PREFIX}/config-info**: Configuration details and auto-detected paths
- **GET /{URL_PREFIX}/test-data**: CSV loading test and diagnostics

### Static Assets
- **GET /{URL_PREFIX}/static/{filename}**: Static file serving (auto-configured)

## Directory Structure

### Automatic Detection

The blueprint automatically locates these directories relative to its location:

```
your_project/
├── heatmap_blueprint.py    # Blueprint file location (reference point)
├── colors/                 # Auto-detected: color schemes
│   ├── colors.json
│   └── colors.min.json
├── static/                 # Auto-detected: CSS, JS, images
│   └── *.png
└── templates/             # Auto-detected: HTML templates
    └── map.html
```

### Override Detection

If auto-detection doesn't work for your structure:

```python
register_heatmap(app,
    COLORS_DIR='/absolute/path/to/colors',
    STATIC_FOLDER='relative/static',
    TEMPLATE_FOLDER='relative/templates'
)
```

### Fallback Behavior

When directories are missing:
- **colors/**: Uses embedded default color schemes
- **static/**: Serves from fallback locations
- **templates/**: Uses minimal embedded templates

## Integration Patterns

### Pattern 1: Standalone Heatmap App

```python
from flask import Flask
from heatmap_blueprint import register_heatmap

app = Flask(__name__)

register_heatmap(app, INPUT_CSV_FILE='survey_data.csv')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Pattern 2: Heatmap Module in Larger App

```python
from flask import Flask, render_template
from heatmap_blueprint import register_heatmap

app = Flask(__name__)

# Main application routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

# Heatmap module
register_heatmap(app,
    CSV_FILES={'Acoustic Data': 'data/acoustic.csv'},
    URL_PREFIX='/visualization'
)

if __name__ == '__main__':
    app.run(debug=True)
```

### Pattern 3: Multiple Heatmap Instances

```python
from flask import Flask
from heatmap_blueprint import register_heatmap

app = Flask(__name__)

register_heatmap(app,
    CSV_FILES={'Acoustic Data 1': 'data/data1.csv'},
    URL_PREFIX='/map1',
    BLUEPRINT_NAME='data1_heatmap',
    INITIAL_HEATMAP_INTENSITY=2.0
)

register_heatmap(app,
    CSV_FILES={'Acoustic Data 2': 'data/data2.csv'},
    URL_PREFIX='/map2',
    BLUEPRINT_NAME='data2_heatmap',
    INITIAL_HEATMAP_RADIUS=60
)

if __name__ == '__main__':
    app.run(debug=True)
```

## Troubleshooting

### Debug Information

Access detailed configuration and status information:

**URL**: `http://your-app/{URL_PREFIX}/config-info`

**Information provided**:
- Configuration sources and values
- Auto-detected directory paths
- CSV file status and errors
- Blueprint registration details

### CSV Testing

Test CSV file loading and format detection:

**URL**: `http://your-app/{URL_PREFIX}/test-data`

**Information provided**:
- CSV file structure analysis
- Column detection results
- Sample data preview
- Loading errors with specific suggestions

### Common Issues

#### CSV File Not Found
**Error**: File path resolution issues
**Solution**: 
- Verify file paths are relative to your Flask app root
- Check file permissions
- Use debug endpoint to verify detected paths

#### Multiple Blueprint Registration
**Error**: Blueprint name conflicts
**Solution**:
```python
register_heatmap(app,
    BLUEPRINT_NAME='unique_name_1',  # Must be unique
    URL_PREFIX='/path1'
)

register_heatmap(app,
    BLUEPRINT_NAME='unique_name_2',  # Different name
    URL_PREFIX='/path2'
)
```

#### Missing Resource Directories
**Error**: Static files or templates not found
**Solution**: The blueprint handles this automatically with fallbacks. Use manual configuration only if needed:
```python
register_heatmap(app,
    STATIC_FOLDER='path/to/static',
    TEMPLATE_FOLDER='path/to/templates'
)
```

#### CSV Format Issues
**Error**: Column detection failures
**Solution**: Verify your CSV has required columns (default: Latitude, Longitude, Value) or specify custom columns:
```python
register_heatmap(app,
    REQUIRED_COLUMNS=['Lat', 'Lng', 'Sound_Level']
)
```

### Error Messages

The blueprint provides detailed error messages with:
- **File preview** for CSV issues
- **Path information** for missing resources
- **Specific suggestions** for resolving problems
- **Auto-detected alternatives** when available

## Migration Guide

### From Standalone App to Blueprint

If you're converting from a standalone Flask app:

1. **Replace app creation**:
   ```python
   # Old
   app = Flask(__name__)
   
   # New
   from heatmap_blueprint import register_heatmap
   register_heatmap(app, ...)
   ```

2. **Update route references**:
   - Old: `http://app/`
   - New: `http://app/{URL_PREFIX}/`

3. **Update configuration**:
   - Move settings to `register_heatmap()` parameters
   - Or use global `config.json`

### From Manual Integration to Auto-Detection

Replace manual path configuration:

```python
# Old manual configuration
register_heatmap(app,
    COLORS_DIR='/path/to/colors',
    STATIC_FOLDER='/path/to/static',
    TEMPLATE_FOLDER='/path/to/templates'
)

# New auto-detection (recommended)
register_heatmap(app, INPUT_CSV_FILE='data.csv')
```

## Support and Resources

### Example Applications

See the `examples/` directory for complete integration examples:
- `minimal_friction_example.py`: Basic integration
- `multiple_csv_dropdown.py`: Multi-dataset setup
- `advanced_configuration.py`: Complex configurations
- `flask_app_integration_example.py`: Full application integration

### Configuration Reference

Complete parameter documentation available in the main `README.md` file.

### Debug Tools

Built-in debug endpoints provide comprehensive troubleshooting information:
- Configuration validation
- Path detection verification  
- CSV format analysis
- Error diagnosis with suggestions 