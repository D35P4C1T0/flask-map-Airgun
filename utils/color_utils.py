import os
import json

COLORS_DIR = 'colors'
ORIGINAL_COLORS_FILE = os.path.join(COLORS_DIR, 'colors.json')
MINIFIED_COLORS_FILE = os.path.join(COLORS_DIR, 'colors.min.json')

DEFAULT_COLORS = [[0, "#80D6EA"], [1, "#8B0000"]]

def load_colors():
    """
    Loads colors from 'colors/colors.json', minifies them,
    writes them to 'colors/colors.min.json', and returns the data.
    Falls back to default colors if any step fails.
    """
    if not os.path.exists(COLORS_DIR):
        try:
            os.makedirs(COLORS_DIR)
            print(f"Created directory: {COLORS_DIR}")
        except OSError as e:
            print(f"Error creating directory {COLORS_DIR}: {e}. Using default colors.")
            return DEFAULT_COLORS

    try:
        with open(ORIGINAL_COLORS_FILE, 'r') as f:
            colors_data = json.load(f)
        print(f"Successfully loaded colors from {ORIGINAL_COLORS_FILE}")

        try:
            with open(MINIFIED_COLORS_FILE, 'w') as f:
                json.dump(colors_data, f, separators=(',', ':'))
            print(f"Successfully minified and saved colors to {MINIFIED_COLORS_FILE}")
        except IOError as e_write:
            print(f"Error writing minified colors to {MINIFIED_COLORS_FILE}: {e_write}. Using loaded data from original if available, otherwise default.")
            # If write fails, we can still proceed with colors_data if it was loaded.
            # The problem statement implies re-creation for use, so disk persistence is secondary to availability for the current run.

        return colors_data

    except FileNotFoundError:
        print(f"Error: {ORIGINAL_COLORS_FILE} not found. Using default colors.")
        return DEFAULT_COLORS
    except json.JSONDecodeError as e_decode:
        print(f"Error decoding JSON from {ORIGINAL_COLORS_FILE}: {e_decode}. Using default colors.")
        return DEFAULT_COLORS
    except Exception as e_read: # Catch any other reading related errors
        print(f"Error reading {ORIGINAL_COLORS_FILE}: {e_read}. Using default colors.")
        return DEFAULT_COLORS 