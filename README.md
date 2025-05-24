# Interactive Heatmap Visualizer

A modern Flask-based web application that creates interactive, real-time heatmap visualizations from CSV data using Deck.gl. The application features a sleek, responsive interface with live parameter controls and smooth animations.

## Features

### Core Functionality
- **Real-time Interactive Heatmaps**: Dynamic heatmap rendering directly in the browser using Deck.gl
- **Sound Propagation Simulation**: Interactive visualization showing how sound propagates through noise barriers
- **Live Parameter Controls**: Adjust heatmap properties in real-time without page reloads:
  - Layer opacity slider
  - Point radius control
  - Intensity adjustment
  - Threshold filtering
- **Responsive Design**: Modern glassmorphism UI with Tailwind CSS
- **Data Visualization**: Supports CSV data with Latitude, Longitude, and Value columns

### User Interface
- **Modern Dashboard**: Clean, professional interface with glassmorphism effects
- **Interactive Controls**: Intuitive sliders and toggles for all heatmap parameters
- **Animation Timeline**: Scrub through sound propagation with play/pause controls and keyboard shortcuts
- **Real-time Feedback**: Instant visual updates as parameters change
- **Responsive Layout**: Works seamlessly on desktop and mobile devices
- **Smooth Animations**: Fluid transitions and hover effects

### Technical Features
- **High Performance**: Client-side rendering with WebGL acceleration via Deck.gl
- **Configurable Color Schemes**: JSON-based color scale definitions
- **Compressed Data Transfer**: Optimized data loading with Flask-Compress
- **CORS Support**: Cross-origin resource sharing enabled
- **Error Handling**: Robust error handling for data loading and processing

## Project Structure

```
├── app.py                 # Main Flask application with API routes
├── config.py             # Configuration management and AppConfig class
├── config.json           # User-configurable application settings
├── requirements.txt      # Python dependencies
├── README.md            # This documentation
├── .gitignore           # Git ignore patterns
├── templates/
│   └── index.html       # Main dashboard template with Deck.gl integration
├── static/              # Static assets (generated raster images, if any)
├── utils/
│   └── color_utils.py   # Color scheme loading and management
├── colors/
│   ├── colors.json      # Color scale definitions
│   └── colors.min.json  # Minified color schemes (auto-generated)
├── data/
│   └── data.csv         # Input dataset (Latitude, Longitude, Value)
└── venv/               # Python virtual environment
```

## Configuration

The application uses a flexible configuration system with `config.json` for user settings and `config.py` for defaults.

### Key Configuration Options

Edit `config.json` to customize the application (create this file if it doesn't exist):

```json
{
    "INPUT_CSV_FILE": "data/data.csv",
    "DEFAULT_MAP_OPACITY": 0.75,
    "INITIAL_HEATMAP_RADIUS": 40,
    "INITIAL_HEATMAP_INTENSITY": 1.5,
    "INITIAL_HEATMAP_THRESHOLD": 0.00,
    "STATIC_FOLDER": "static",
    "FRONTEND_TEMPLATE": "index.html",
    "REQUIRED_COLUMNS": ["Latitude", "Longitude", "Value"]
}
```

### Configuration Parameters

- **INPUT_CSV_FILE**: Path to your CSV data file
- **DEFAULT_MAP_OPACITY**: Initial opacity for the heatmap layer (0.0-1.0)
- **INITIAL_HEATMAP_RADIUS**: Default radius for heatmap points
- **INITIAL_HEATMAP_INTENSITY**: Default intensity multiplier
- **INITIAL_HEATMAP_THRESHOLD**: Minimum value threshold for display
- **REQUIRED_COLUMNS**: Expected column names in the CSV file

## Data Format

Your CSV file must contain the following columns:
- **Latitude**: Geographic latitude coordinates
- **Longitude**: Geographic longitude coordinates  
- **Value**: Numeric values to visualize in the heatmap (interpreted as noise levels for propagation simulation)

Example CSV structure:
```csv
Latitude,Longitude,Value
40.7128,-74.0060,25.3
40.7589,-73.9851,18.7
40.6892,-74.0445,31.2
```

## Sound Propagation Simulation

The application includes a sophisticated sound propagation visualization that demonstrates how sound waves travel through areas with varying noise resistance.

### How It Works

1. **Sound Source**: The simulation calculates a weighted center point based on inverse noise values (areas with less noise become the optimal sound source location)

2. **Propagation Physics**: 
   - Sound travels outward from the center point
   - Higher noise values create resistance, slowing down sound propagation
   - Sound intensity decreases with distance and time
   - Areas with high noise act as barriers

3. **Visual Representation**:
   - **Yellow marker**: Sound source location
   - **Colored points**: Sound intensity at each location over time
   - **Color coding**: Red/orange for high intensity, blue for low intensity
   - **Size**: Point size represents sound intensity

### Interactive Controls

- **Play/Pause Button**: Start or stop the animation
- **Reset Button**: Return to the beginning of the simulation
- **Timeline Slider**: Scrub through any point in the 10-second animation
- **Keyboard Shortcuts**:
  - `Space`: Play/pause animation
  - `←/→`: Step backward/forward one frame
  - `R`: Reset to beginning

### Technical Details

- **100 time steps** over a 10-second simulation
- **Physics-based calculation** considering distance and noise resistance
- **Real-time rendering** with WebGL acceleration
- **Optimized data processing** for smooth animation performance

## Setup and Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd heatmap-airgun
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare your data**
   - Place your CSV file in the `data/` directory
   - Ensure it has the required columns: Latitude, Longitude, Value
   - Update `config.json` if using a different filename

5. **Configure color schemes (optional)**
   - Modify `colors/colors.json` to customize the heatmap color scale
   - The application will auto-generate a minified version

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://127.0.0.1:5000/` (or the address shown in the terminal)

3. **Interact with the visualizations**
   - **Heatmap View**: Use the control panel on the right to adjust heatmap parameters
   - **Sound Propagation**: Click "Sound Propagation" button to view the animation
   - Pan and zoom the map to explore your data
   - Use keyboard shortcuts for quick navigation

## API Endpoints

- **GET /**: Main heatmap dashboard page
- **GET /propagation**: Sound propagation visualization page
- **GET /data**: Returns CSV data as JSON with value range and color scale
- **GET /propagation-data**: Returns computed sound propagation simulation data
- **GET /static/<filename>**: Serves static assets

## Dependencies

Key Python packages:
- **Flask**: Web framework
- **pandas**: Data manipulation and CSV processing
- **Flask-CORS**: Cross-origin resource sharing
- **Flask-Compress**: Response compression
- **PyYAML**: YAML configuration support (optional)

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
- Data is compressed during transfer to minimize loading times
- Color schemes are minified automatically for faster loading

## Troubleshooting

### Common Issues

1. **CSV file not found**: Ensure your data file exists in the `data/` directory
2. **Missing columns**: Verify your CSV has Latitude, Longitude, and Value columns
3. **Performance issues**: Try reducing the radius or intensity for large datasets
4. **Browser compatibility**: Ensure WebGL is enabled in your browser

### Debug Mode

Run the application in debug mode for detailed error messages:
```bash
python app.py
```
Debug mode is enabled by default in the current configuration. 