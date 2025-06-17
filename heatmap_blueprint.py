import os
import json
import pandas as pd
import numpy as np
from flask import Blueprint, jsonify, send_from_directory, render_template, request, current_app
from flask_compress import Compress

class HeatmapConfig:
    """Configuration class for the heatmap blueprint"""
    def __init__(self, **kwargs):
        # CSV file configuration - supports both single file and multiple files
        self.INPUT_CSV_FILE = kwargs.get('INPUT_CSV_FILE', 'data/data.csv')  # Backward compatibility
        self.CSV_FILES = kwargs.get('CSV_FILES', None)  # New: dict of {name: filepath} or list of filepaths
        self.DEFAULT_CSV = kwargs.get('DEFAULT_CSV', None)  # Which CSV to show by default
        
        # Folder configuration
        self.STATIC_FOLDER = kwargs.get('STATIC_FOLDER', 'static')
        self.TEMPLATE_FOLDER = kwargs.get('TEMPLATE_FOLDER', 'templates')
        self.COLORS_DIR = kwargs.get('COLORS_DIR', 'colors')
        
        # Data configuration
        self.REQUIRED_COLUMNS = kwargs.get('REQUIRED_COLUMNS', ['Latitude', 'Longitude', 'Value'])
        self.DEFAULT_MAP_OPACITY = kwargs.get('DEFAULT_MAP_OPACITY', 0.75)
        self.INITIAL_HEATMAP_RADIUS = kwargs.get('INITIAL_HEATMAP_RADIUS', 40)
        self.INITIAL_HEATMAP_INTENSITY = kwargs.get('INITIAL_HEATMAP_INTENSITY', 1.5)
        self.INITIAL_HEATMAP_THRESHOLD = kwargs.get('INITIAL_HEATMAP_THRESHOLD', 0.00)
        
        # Blueprint configuration
        self.URL_PREFIX = kwargs.get('URL_PREFIX', '/heatmap')
        self.BLUEPRINT_NAME = kwargs.get('BLUEPRINT_NAME', 'heatmap')
        
        # Process CSV files configuration
        self._process_csv_files()
    
    def _process_csv_files(self):
        """Process and normalize CSV files configuration"""
        if self.CSV_FILES is None:
            # Backward compatibility: single file mode
            self.csv_files_dict = {'Default': self.INPUT_CSV_FILE}
            self.default_csv_key = 'Default'
        elif isinstance(self.CSV_FILES, dict):
            # Dictionary mode: {display_name: filepath}
            self.csv_files_dict = self.CSV_FILES.copy()
            self.default_csv_key = self.DEFAULT_CSV or list(self.csv_files_dict.keys())[0]
        elif isinstance(self.CSV_FILES, list):
            # List mode: [filepath1, filepath2, ...]
            import os
            self.csv_files_dict = {}
            for filepath in self.CSV_FILES:
                # Use filename without extension as display name
                display_name = os.path.splitext(os.path.basename(filepath))[0]
                self.csv_files_dict[display_name] = filepath
            self.default_csv_key = self.DEFAULT_CSV or list(self.csv_files_dict.keys())[0]
        else:
            raise ValueError("CSV_FILES must be a dict or list")
        
        # Validate default CSV
        if self.default_csv_key not in self.csv_files_dict:
            self.default_csv_key = list(self.csv_files_dict.keys())[0]
    
    def get_csv_files(self):
        """Get the dictionary of available CSV files"""
        return self.csv_files_dict
    
    def get_csv_path(self, csv_key):
        """Get the file path for a specific CSV key"""
        return self.csv_files_dict.get(csv_key)

def load_colors(colors_dir='colors'):
    """
    Loads colors from colors directory, returns default if not found.
    """
    colors_file = os.path.join(colors_dir, 'colors.json')
    default_colors = [[0, "#80D6EA"], [1, "#8B0000"]]
    
    try:
        if os.path.exists(colors_file):
            with open(colors_file, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading colors from {colors_file}: {e}")
    
    return default_colors

def create_heatmap_blueprint(config=None):
    """
    Factory function to create a heatmap blueprint with custom configuration.
    
    Args:
        config: HeatmapConfig instance or dict with configuration options
    
    Returns:
        Flask Blueprint instance
    """
    
    # Handle configuration
    if config is None:
        config = HeatmapConfig()
    elif isinstance(config, dict):
        config = HeatmapConfig(**config)
    elif not isinstance(config, HeatmapConfig):
        raise ValueError("config must be HeatmapConfig instance or dict")
    
    # Create blueprint
    bp = Blueprint(
        config.BLUEPRINT_NAME,
        __name__,
        url_prefix=config.URL_PREFIX,
        template_folder=config.TEMPLATE_FOLDER,
        static_folder=config.STATIC_FOLDER,
        static_url_path=f'{config.URL_PREFIX}/static'
    )
    
    @bp.route('/')
    def index():
        return render_template('map.html', config=config)

    @bp.route('/propagation')
    def propagation():
        return render_template('propagation.html', config=config)

    @bp.route('/csv-files')
    def get_csv_files():
        """Get list of available CSV files"""
        try:
            csv_files = config.get_csv_files()
            return jsonify({
                'files': csv_files,
                'default': config.default_csv_key
            })
        except Exception as e:
            print(f"Error in get_csv_files: {e}")
            return jsonify({'error': str(e)}), 500

    @bp.route('/data')
    @bp.route('/data/<csv_key>')
    def get_data(csv_key=None):
        try:
            # Use default CSV if no key specified
            if csv_key is None:
                csv_key = config.default_csv_key
            
            # Get CSV file path
            csv_file = config.get_csv_path(csv_key)
            if csv_file is None:
                return jsonify({'error': f'CSV file not found: {csv_key}'}), 404
            
            print(f"Loading data from: {csv_file}")
            
            # Read CSV file (skip the first column which is an index)
            df = pd.read_csv(csv_file, index_col=0)
            
            # Extract required columns
            data = df[config.REQUIRED_COLUMNS].to_dict(orient='records')
            
            # Calculate data range for the heatmap
            min_val = float(df['Value'].min())
            max_val = float(df['Value'].max())
            value_range = {
                'min': min_val,
                'max': max_val
            }
            
            print(f"Data range for {csv_key}: min={min_val}, max={max_val}")
            print(f"Sample values: {df['Value'].head().tolist()}")
            
            # Load color configuration
            colors = load_colors(config.COLORS_DIR)
            
            response_data = {
                'data': data,
                'valueRange': value_range,
                'colorScale': colors,
                'csvKey': csv_key,
                'csvFile': csv_file
            }
            
            return jsonify(response_data)
        except Exception as e:
            print(f"Error in get_data: {e}")
            return jsonify({'error': str(e)}), 500

    @bp.route('/propagation-data')
    @bp.route('/propagation-data/<csv_key>')
    def get_propagation_data(csv_key=None):
        try:
            # Use default CSV if no key specified
            if csv_key is None:
                csv_key = config.default_csv_key
            
            # Get CSV file path
            csv_file = config.get_csv_path(csv_key)
            if csv_file is None:
                return jsonify({'error': f'CSV file not found: {csv_key}'}), 404
            
            # Read CSV file (skip the first column which is an index)
            df = pd.read_csv(csv_file, index_col=0)
            print(f"Loading propagation data: {len(df)} points")
            
            # Check if we have the required columns
            for col in config.REQUIRED_COLUMNS:
                if col not in df.columns:
                    raise ValueError(f"Missing required column: {col}")
            
            # Remove any rows with NaN values
            df_clean = df.dropna(subset=config.REQUIRED_COLUMNS)
            
            if len(df_clean) == 0:
                raise ValueError("No valid data points found after removing NaN values")
            
            # Sample the data to make it manageable
            sample_factor = max(1, len(df_clean) // 2000)  # Limit to ~2000 points for better performance
            df_sampled = df_clean.iloc[::sample_factor].copy().reset_index(drop=True)
            print(f"Processing {len(df_sampled)} sampled points")
            
            if len(df_sampled) == 0:
                raise ValueError("No data points after sampling")
            
            # Calculate center point (simple geographic center)
            try:
                center_lat = float(df_sampled['Latitude'].mean())
                center_lon = float(df_sampled['Longitude'].mean())
                
                if not (np.isfinite(center_lat) and np.isfinite(center_lon)):
                    raise ValueError("Invalid center coordinates calculated")
                    
            except Exception as e:
                raise ValueError(f"Error calculating center point: {str(e)}")
            
            # Calculate distances from center
            try:
                lat_diff = df_sampled['Latitude'] - center_lat
                lon_diff = df_sampled['Longitude'] - center_lon
                distances = np.sqrt(lat_diff**2 + lon_diff**2)
                
                if not np.all(np.isfinite(distances)):
                    raise ValueError("Invalid distances calculated")
                    
            except Exception as e:
                raise ValueError(f"Error calculating distances: {str(e)}")
            
            # Normalize noise values (0 to 1)
            try:
                min_noise = float(df_sampled['Value'].min())
                max_noise = float(df_sampled['Value'].max())
                
                if not (np.isfinite(min_noise) and np.isfinite(max_noise)):
                    raise ValueError("Invalid noise values found")
                
                if max_noise == min_noise:
                    # Handle case where all values are the same
                    resistance = np.zeros(len(df_sampled))
                else:
                    resistance = (df_sampled['Value'] - min_noise) / (max_noise - min_noise)
                    
                    if not np.all(np.isfinite(resistance)):
                        raise ValueError("Invalid resistance values calculated")
                        
            except Exception as e:
                raise ValueError(f"Error normalizing noise values: {str(e)}")
            
            max_distance = float(distances.max())
            if max_distance == 0 or not np.isfinite(max_distance):
                max_distance = 1.0  # Prevent division by zero
            
            # Create propagation simulation
            time_steps = 30  # Increased for smoother animation
            
            propagation_frames = []
            
            try:
                for step in range(time_steps):
                    # Current time (0 to 1)
                    current_time = step / max(1, time_steps - 1) if time_steps > 1 else 0
                    
                    # Smooth wave propagation
                    normalized_distances = distances / max_distance
                    
                    # Smooth resistance effect
                    arrival_times = normalized_distances + (resistance * 0.3)
                    
                    # Smooth wave front calculation
                    wave_progress = current_time * 1.2  # Wave speed
                    
                    # Calculate smooth intensities for all points
                    distance_factors = np.maximum(0, 1 - normalized_distances)
                    resistance_factors = np.maximum(0.2, 1 - resistance * 0.8)
                    
                    # Smooth wave intensity based on distance from wave front
                    wave_front_distance = np.abs(normalized_distances - wave_progress)
                    wave_intensity = np.exp(-wave_front_distance * 8)  # Sharp wave front
                    
                    # Combine factors for smooth propagation
                    base_intensity = distance_factors * resistance_factors * wave_intensity
                    
                    # Add subtle wave oscillation for realism
                    wave_phase = (current_time * 4 - normalized_distances * 2) * np.pi
                    wave_modulation = 1 + 0.1 * np.sin(wave_phase)
                    
                    intensities = base_intensity * wave_modulation
                    
                    # Filter for meaningful points with smooth threshold
                    meaningful_mask = intensities > 0.05
                    
                    if not np.any(meaningful_mask):
                        propagation_frames.append([])
                        continue
                    
                    # Create smooth frame data
                    meaningful_indices = np.where(meaningful_mask)[0]
                    
                    frame_data = []
                    for idx in meaningful_indices:
                        try:
                            lat_val = float(df_sampled.iloc[idx]['Latitude'])
                            lon_val = float(df_sampled.iloc[idx]['Longitude'])
                            intensity_val = float(intensities[idx])
                            noise_val = float(df_sampled.iloc[idx]['Value'])
                            distance_val = float(distances[idx])
                            
                            # Validate all values are finite
                            if all(np.isfinite([lat_val, lon_val, intensity_val, noise_val, distance_val])):
                                frame_data.append({
                                    'latitude': lat_val,
                                    'longitude': lon_val,
                                    'intensity': intensity_val,
                                    'noise': noise_val,
                                    'distance': distance_val
                                })
                        except Exception as e:
                            print(f"Warning: Skipping invalid data point at index {idx}: {e}")
                            continue
                    
                    propagation_frames.append(frame_data)
                    
            except Exception as e:
                raise ValueError(f"Error during propagation simulation: {str(e)}")
            
            response_data = {
                'frames': propagation_frames,
                'center': {'latitude': center_lat, 'longitude': center_lon},
                'maxDistance': max_distance,
                'timeSteps': time_steps,
                'valueRange': {
                    'min': min_noise,
                    'max': max_noise
                },
                'sampleInfo': {
                    'originalPoints': len(df),
                    'sampledPoints': len(df_sampled),
                    'sampleFactor': sample_factor
                }
            }
            
            print(f"Propagation calculation completed successfully with {len(propagation_frames)} frames")
            return jsonify(response_data)
            
        except Exception as e:
            error_message = str(e) if str(e) else "Unknown error occurred"
            print(f"Error in propagation calculation: {error_message}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f"Propagation calculation failed: {error_message}"}), 500

    @bp.route('/test-data')
    @bp.route('/test-data/<csv_key>')
    def test_data(csv_key=None):
        try:
            # Use default CSV if no key specified
            if csv_key is None:
                csv_key = config.default_csv_key
            
            # Get CSV file path
            csv_file = config.get_csv_path(csv_key)
            if csv_file is None:
                return jsonify({'error': f'CSV file not found: {csv_key}'}), 404
            
            df = pd.read_csv(csv_file, index_col=0)
            return jsonify({
                'success': True,
                'csvKey': csv_key,
                'csvFile': csv_file,
                'rows': len(df),
                'columns': df.columns.tolist(),
                'sample': df.head(3).to_dict('records')
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory(config.STATIC_FOLDER, filename)
    
    return bp

# Convenience function for simple integration
def register_heatmap(app, **config_kwargs):
    """
    Simple function to register heatmap blueprint with a Flask app.
    
    Args:
        app: Flask application instance
        **config_kwargs: Configuration options for HeatmapConfig
    
    Returns:
        The registered blueprint instance
    """
    blueprint = create_heatmap_blueprint(config_kwargs)
    app.register_blueprint(blueprint)
    return blueprint 