import os
import json
import pandas as pd
import numpy as np
from flask import Blueprint, jsonify, send_from_directory, render_template, request, current_app
from flask_compress import Compress

# Import the global configuration system
try:
    from config import AppConfig
    GLOBAL_CONFIG_AVAILABLE = True
except ImportError:
    GLOBAL_CONFIG_AVAILABLE = False
    # Fallback defaults if config.py is not available
    class AppConfig:
        INPUT_CSV_FILE = 'data/data.csv'
        STATIC_FOLDER = 'static'
        TEMPLATE_FOLDER = 'templates'
        REQUIRED_COLUMNS = ['Latitude', 'Longitude', 'Value']
        DEFAULT_MAP_OPACITY = 0.75
        INITIAL_HEATMAP_RADIUS = 40
        INITIAL_HEATMAP_INTENSITY = 1.5
        INITIAL_HEATMAP_THRESHOLD = 0.00

def get_blueprint_directory():
    """Get the directory where this blueprint file is located"""
    return os.path.dirname(os.path.abspath(__file__))

def auto_detect_resource_paths():
    """
    Auto-detect paths for colors, static, and templates relative to blueprint location.
    This eliminates the need to manually specify these paths during integration.
    """
    blueprint_dir = get_blueprint_directory()
    
    paths = {
        'colors': os.path.join(blueprint_dir, 'colors'),
        'static': os.path.join(blueprint_dir, 'static'), 
        'templates': os.path.join(blueprint_dir, 'templates')
    }
    
    # Verify paths exist and provide fallbacks
    for key, path in paths.items():
        if not os.path.exists(path):
            print(f"⚠ Warning: {key} directory not found at {path}")
            # Try alternative locations
            alt_path = os.path.join(os.getcwd(), key)
            if os.path.exists(alt_path):
                paths[key] = alt_path
                print(f"✓ Using alternative {key} directory: {alt_path}")
            else:
                print(f"ℹ Using default {key} path: {path}")
    
    return paths

def smart_csv_read(csv_file, required_columns):
    """
    Intelligently read CSV files with flexible format handling.
    Handles files with or without index columns automatically.
    """
    print(f"📊 Smart CSV reading: {csv_file}")
    
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")
    
    # First, try to read with index_col=0 (current default behavior)
    try:
        df = pd.read_csv(csv_file, index_col=0)
        print(f"✓ CSV read with index column, shape: {df.shape}")
        
        # Check if required columns exist
        missing_cols = [col for col in required_columns if col not in df.columns]
        if not missing_cols:
            print(f"✓ All required columns found: {required_columns}")
            return df
        else:
            print(f"⚠ Missing columns with index_col=0: {missing_cols}")
            
    except Exception as e:
        print(f"⚠ Failed to read with index_col=0: {e}")
    
    # Try reading without index column
    try:
        df = pd.read_csv(csv_file)
        print(f"✓ CSV read without index column, shape: {df.shape}")
        print(f"Available columns: {list(df.columns)}")
        
        # Check if required columns exist
        missing_cols = [col for col in required_columns if col not in df.columns]
        if not missing_cols:
            print(f"✓ All required columns found: {required_columns}")
            return df
        else:
            print(f"⚠ Missing required columns: {missing_cols}")
            
    except Exception as e:
        print(f"⚠ Failed to read without index: {e}")
    
    # Try with different encodings if standard reading fails
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        try:
            df = pd.read_csv(csv_file, encoding=encoding)
            print(f"✓ CSV read with {encoding} encoding, shape: {df.shape}")
            
            missing_cols = [col for col in required_columns if col not in df.columns]
            if not missing_cols:
                print(f"✓ All required columns found with {encoding} encoding")
                return df
                
        except Exception as e:
            print(f"⚠ Failed with {encoding} encoding: {e}")
            continue
    
    # If we get here, we couldn't read the file properly
    try:
        # Last resort: read first few lines to show structure
        with open(csv_file, 'r') as f:
            preview = f.read(500)
        raise ValueError(f"Could not read CSV file. Required columns: {required_columns}. File preview:\n{preview}")
    except:
        raise ValueError(f"Could not read CSV file: {csv_file}. Required columns: {required_columns}")

class HeatmapConfig:
    """
    Unified configuration class for the heatmap blueprint.
    
    Priority order:
    1. Runtime parameters (**kwargs) - highest priority
    2. Global config.json/AppConfig - fallback defaults
    3. Hardcoded defaults - lowest priority
    
    This allows for:
    - Global configuration via config.json
    - Per-instance overrides via register_heatmap() parameters
    - Multiple blueprint instances with different configs
    - Auto-detection of resource paths for minimal friction
    """
    def __init__(self, **kwargs):
        # Auto-detect resource paths if not provided
        auto_paths = auto_detect_resource_paths()
        
        # Load global configuration defaults first
        global_defaults = self._load_global_defaults()
        
        # CSV file configuration - supports both single file and multiple files
        self.INPUT_CSV_FILE = kwargs.get('INPUT_CSV_FILE', global_defaults.get('INPUT_CSV_FILE', 'data/data.csv'))
        self.CSV_FILES = kwargs.get('CSV_FILES', None)  # New: dict of {name: filepath} or list of filepaths
        self.DEFAULT_CSV = kwargs.get('DEFAULT_CSV', None)  # Which CSV to show by default
        
        # Folder configuration with auto-detection
        self.STATIC_FOLDER = kwargs.get('STATIC_FOLDER', global_defaults.get('STATIC_FOLDER', auto_paths['static']))
        self.TEMPLATE_FOLDER = kwargs.get('TEMPLATE_FOLDER', global_defaults.get('TEMPLATE_FOLDER', auto_paths['templates']))
        self.COLORS_DIR = kwargs.get('COLORS_DIR', auto_paths['colors'])
        
        # Data configuration
        self.REQUIRED_COLUMNS = kwargs.get('REQUIRED_COLUMNS', global_defaults.get('REQUIRED_COLUMNS', ['Latitude', 'Longitude', 'Value']))
        self.DEFAULT_MAP_OPACITY = kwargs.get('DEFAULT_MAP_OPACITY', global_defaults.get('DEFAULT_MAP_OPACITY', 0.75))
        self.INITIAL_HEATMAP_RADIUS = kwargs.get('INITIAL_HEATMAP_RADIUS', global_defaults.get('INITIAL_HEATMAP_RADIUS', 40))
        self.INITIAL_HEATMAP_INTENSITY = kwargs.get('INITIAL_HEATMAP_INTENSITY', global_defaults.get('INITIAL_HEATMAP_INTENSITY', 1.5))
        self.INITIAL_HEATMAP_THRESHOLD = kwargs.get('INITIAL_HEATMAP_THRESHOLD', global_defaults.get('INITIAL_HEATMAP_THRESHOLD', 0.00))
        
        # Blueprint configuration (these are blueprint-specific, no global defaults)
        self.URL_PREFIX = kwargs.get('URL_PREFIX', '/heatmap')
        self.BLUEPRINT_NAME = kwargs.get('BLUEPRINT_NAME', 'heatmap')
        
        # Process CSV files configuration
        self._process_csv_files()
        
        # Store configuration source info for debugging
        self._config_sources = {
            'global_config_available': GLOBAL_CONFIG_AVAILABLE,
            'runtime_overrides': list(kwargs.keys()) if kwargs else [],
            'using_global_defaults': bool(global_defaults),
            'auto_detected_paths': auto_paths
        }
        
        # Print setup info for debugging
        print(f"🔧 Blueprint setup: {self.BLUEPRINT_NAME}")
        print(f"   Colors: {self.COLORS_DIR}")
        print(f"   Static: {self.STATIC_FOLDER}")
        print(f"   Templates: {self.TEMPLATE_FOLDER}")
        print(f"   CSV files: {len(self.csv_files_dict)} dataset(s)")
    
    def _load_global_defaults(self):
        """
        Load configuration defaults from the global AppConfig system.
        
        Returns:
            dict: Dictionary of default values from global config
        """
        defaults = {}
        
        if GLOBAL_CONFIG_AVAILABLE:
            try:
                # Extract relevant configuration from AppConfig
                config_attrs = [
                    'INPUT_CSV_FILE', 'STATIC_FOLDER', 'FRONTEND_TEMPLATE', 
                    'REQUIRED_COLUMNS', 'DEFAULT_MAP_OPACITY', 
                    'INITIAL_HEATMAP_RADIUS', 'INITIAL_HEATMAP_INTENSITY', 
                    'INITIAL_HEATMAP_THRESHOLD'
                ]
                
                for attr in config_attrs:
                    if hasattr(AppConfig, attr):
                        defaults[attr] = getattr(AppConfig, attr)
                
                # Map FRONTEND_TEMPLATE to TEMPLATE_FOLDER for compatibility
                if 'FRONTEND_TEMPLATE' in defaults:
                    defaults['TEMPLATE_FOLDER'] = 'templates'
                
                print(f"✓ Loaded global configuration defaults: {list(defaults.keys())}")
                
            except Exception as e:
                print(f"⚠ Warning: Error loading global config: {e}")
        else:
            print("ℹ Global config (config.py) not available, using hardcoded defaults")
        
        return defaults
    
    def get_config_info(self):
        """
        Get information about how this configuration was loaded.
        Useful for debugging and understanding configuration precedence.
        
        Returns:
            dict: Configuration loading information
        """
        return {
            'sources': self._config_sources,
            'current_values': {
                'INPUT_CSV_FILE': self.INPUT_CSV_FILE,
                'STATIC_FOLDER': self.STATIC_FOLDER,
                'TEMPLATE_FOLDER': self.TEMPLATE_FOLDER,
                'REQUIRED_COLUMNS': self.REQUIRED_COLUMNS,
                'DEFAULT_MAP_OPACITY': self.DEFAULT_MAP_OPACITY,
                'INITIAL_HEATMAP_RADIUS': self.INITIAL_HEATMAP_RADIUS,
                'INITIAL_HEATMAP_INTENSITY': self.INITIAL_HEATMAP_INTENSITY,
                'INITIAL_HEATMAP_THRESHOLD': self.INITIAL_HEATMAP_THRESHOLD,
                'URL_PREFIX': self.URL_PREFIX,
                'BLUEPRINT_NAME': self.BLUEPRINT_NAME,
                'CSV_FILES': self.csv_files_dict,
                'DEFAULT_CSV': self.default_csv_key
            }
        }
    
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
        else:
            print(f"ℹ Colors file not found at {colors_file}, using defaults")
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

    @bp.route('/config-info')
    def get_config_info():
        """Get configuration information and sources (for debugging)"""
        try:
            config_info = config.get_config_info()
            return jsonify(config_info)
        except Exception as e:
            print(f"Error in get_config_info: {e}")
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
            
            print(f"📊 Loading data from: {csv_file}")
            
            # Use smart CSV reading with flexible format handling
            df = smart_csv_read(csv_file, config.REQUIRED_COLUMNS)
            
            # Extract required columns
            data = df[config.REQUIRED_COLUMNS].to_dict(orient='records')
            
            # Calculate data range for the heatmap
            min_val = float(df['Value'].min())
            max_val = float(df['Value'].max())
            value_range = {
                'min': min_val,
                'max': max_val
            }
            
            print(f"✓ Data range for {csv_key}: min={min_val}, max={max_val}")
            print(f"✓ Loaded {len(data)} data points")
            
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
        
        except FileNotFoundError as e:
            error_msg = f"CSV file not found: {e}"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 404
            
        except ValueError as e:
            error_msg = f"CSV format error: {e}"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 400
            
        except Exception as e:
            error_msg = f"Unexpected error loading data: {e}"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 500

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
            
            # Use smart CSV reading with flexible format handling
            df = smart_csv_read(csv_file, config.REQUIRED_COLUMNS)
            print(f"📊 Loading propagation data: {len(df)} points")
            
            # Remove any rows with NaN values
            df_clean = df.dropna(subset=config.REQUIRED_COLUMNS)
            
            if len(df_clean) == 0:
                raise ValueError("No valid data points found after removing NaN values")
            
            # Sample the data to make it manageable
            sample_factor = max(1, len(df_clean) // 2000)  # Limit to ~2000 points for better performance
            df_sampled = df_clean.iloc[::sample_factor].copy().reset_index(drop=True)
            print(f"📊 Processing {len(df_sampled)} sampled points")
            
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
                        except Exception as point_error:
                            print(f"Warning: Skipping invalid point {idx}: {point_error}")
                            continue
                    
                    propagation_frames.append(frame_data)
                    
            except Exception as e:
                print(f"Error in propagation simulation: {e}")
                raise ValueError(f"Error generating propagation simulation: {str(e)}")
            
            # Build response
            response_data = {
                'frames': propagation_frames,
                'centerPoint': [center_lat, center_lon],
                'timeSteps': time_steps,
                'stats': {
                    'totalPoints': len(df_sampled),
                    'minNoise': min_noise,
                    'maxNoise': max_noise,
                    'maxDistance': max_distance
                },
                'csvKey': csv_key,
                'csvFile': csv_file
            }
            
            print(f"✓ Propagation simulation completed: {time_steps} frames, center at ({center_lat:.4f}, {center_lon:.4f})")
            
            return jsonify(response_data)
            
        except FileNotFoundError as e:
            error_msg = f"CSV file not found: {e}"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 404
            
        except ValueError as e:
            error_msg = f"Data processing error: {e}"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 400
            
        except Exception as e:
            error_msg = f"Unexpected error in propagation data: {e}"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 500

    @bp.route('/test-data')
    @bp.route('/test-data/<csv_key>')
    def test_data(csv_key=None):
        """Test endpoint to validate CSV data loading"""
        try:
            if csv_key is None:
                csv_key = config.default_csv_key
            
            csv_file = config.get_csv_path(csv_key)
            if csv_file is None:
                return jsonify({'error': f'CSV file not found: {csv_key}'}), 404
            
            # Test smart CSV reading
            df = smart_csv_read(csv_file, config.REQUIRED_COLUMNS)
            
            return jsonify({
                'csvKey': csv_key,
                'csvFile': csv_file,
                'shape': df.shape,
                'columns': list(df.columns),
                'requiredColumns': config.REQUIRED_COLUMNS,
                'sample': df.head().to_dict(orient='records')
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory(config.STATIC_FOLDER, filename)
    
    return bp

def register_heatmap(app, **config_kwargs):
    """
    Simplified registration function for the heatmap blueprint.
    
    This is the main entry point for adding heatmap functionality to your Flask app.
    Now with minimal friction - just point to your CSV file and go!
    
    Args:
        app: Flask application instance
        **config_kwargs: Configuration parameters (see HeatmapConfig for options)
    
    Example:
        # Minimal usage - just specify your CSV file
        register_heatmap(app, INPUT_CSV_FILE='path/to/your/data.csv')
        
        # Multiple CSV files
        register_heatmap(app, CSV_FILES={
            'Survey 2023': 'data/survey_2023.csv',
            'Survey 2022': 'data/survey_2022.csv'
        })
    """
    config = HeatmapConfig(**config_kwargs)
    blueprint = create_heatmap_blueprint(config)
    app.register_blueprint(blueprint)
    
    print(f"🚀 Heatmap blueprint registered!")
    print(f"   Available at: {config.URL_PREFIX}/")
    print(f"   Propagation: Integrated in main view")
    print(f"   Data API: {config.URL_PREFIX}/data")
    
    return blueprint 