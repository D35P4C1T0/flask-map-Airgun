import os
import json
import yaml # Added for optional YAML support

# --- Default Configuration Values ---
DEFAULT_SETTINGS = {
    'INPUT_CSV_FILE': 'data/data.csv',
    'STATIC_FOLDER': 'static',
    'FRONTEND_TEMPLATE': 'index.html',
    'REQUIRED_COLUMNS': ['Latitude', 'Longitude', 'Value'],
    'DEFAULT_MAP_OPACITY': 0.75,
    'INITIAL_HEATMAP_RADIUS': 40,
    'INITIAL_HEATMAP_INTENSITY': 1.5,
    'INITIAL_HEATMAP_THRESHOLD': 0.00,
}

CONFIG_JSON_FILE_PATH = 'config.json'
CONFIG_YAML_FILE_PATH = 'config.yaml' # Path for optional YAML config
# ENABLE_YAML_CONFIG = False # Flag to enable YAML (kept False for now)

# --- App Configuration Class ---
class AppConfig:
    # Attributes will be set dynamically by _initialize_config
    pass

def _load_and_set_config():
    settings = DEFAULT_SETTINGS.copy() # Start with defaults
    config_loaded_from_file = False

    # Try loading from JSON first
    try:
        with open(CONFIG_JSON_FILE_PATH, 'r') as f:
            json_config = json.load(f)
        settings.update(json_config) # Override defaults with values from JSON
        print(f"Successfully loaded configuration from {CONFIG_JSON_FILE_PATH}")
        config_loaded_from_file = True
    except FileNotFoundError:
        print(f"{CONFIG_JSON_FILE_PATH} not found. Looking for other config types or using defaults.")
    except json.JSONDecodeError as e:
        print(f"Error decoding {CONFIG_JSON_FILE_PATH}: {e}. Using default configuration or last valid one.")
        # Potentially proceed to try YAML or just use defaults already in settings
    except Exception as e:
        print(f"An unexpected error occurred while loading {CONFIG_JSON_FILE_PATH}: {e}. Using defaults.")

    # Placeholder/Commented-out: Optional YAML loading
    # if not config_loaded_from_file and ENABLE_YAML_CONFIG:
    #     try:
    #         with open(CONFIG_YAML_FILE_PATH, 'r') as f:
    #             yaml_config = yaml.safe_load(f)
    #         if yaml_config: # Ensure yaml_config is not None (e.g., empty file)
    #             settings.update(yaml_config)
    #             print(f"Successfully loaded configuration from {CONFIG_YAML_FILE_PATH}")
    #             config_loaded_from_file = True
    #         else:
    #             print(f"{CONFIG_YAML_FILE_PATH} is empty. Using defaults or JSON config (if loaded).")
    #     except FileNotFoundError:
    #         print(f"{CONFIG_YAML_FILE_PATH} not found. Using defaults or JSON config (if loaded).")
    #     except yaml.YAMLError as e:
    #         print(f"Error decoding {CONFIG_YAML_FILE_PATH}: {e}. Using defaults or JSON config (if loaded).")
    #     except Exception as e:
    #         print(f"An unexpected error occurred while loading {CONFIG_YAML_FILE_PATH}: {e}. Using defaults or JSON config (if loaded).")

    if not config_loaded_from_file:
        print("No valid configuration file found. Using default settings.")

    for key, value in settings.items():
        setattr(AppConfig, key, value)

    # Ensure static methods can still access these as class attributes
    # (They are already set by setattr above)

# Initialize configuration when this module is imported
_load_and_set_config()

# Ensure the static folder exists after config is loaded
if hasattr(AppConfig, 'STATIC_FOLDER') and AppConfig.STATIC_FOLDER and not os.path.exists(AppConfig.STATIC_FOLDER):
    try:
        os.makedirs(AppConfig.STATIC_FOLDER)
        print(f"Created static folder: {AppConfig.STATIC_FOLDER}")
    except OSError as e:
        print(f"Error creating static folder {AppConfig.STATIC_FOLDER}: {e}") 