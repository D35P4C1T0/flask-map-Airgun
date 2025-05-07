import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from config import AppConfig # For AppConfig.REQUIRED_COLUMNS

# --- Helper Functions for Data Processing and Plotting ---

def load_and_validate_data(csv_path, required_cols):
    """Loads data from CSV and validates required columns."""
    try:
        df = pd.read_csv(csv_path)
        if not all(col in df.columns for col in required_cols):
            missing_cols = [col for col in required_cols if col not in df.columns]
            return None, f"Missing required columns in CSV: {', '.join(missing_cols)}"
        return df, None
    except FileNotFoundError:
        return None, f"Error: Input CSV file not found at {csv_path}"
    except Exception as e:
        return None, f"Error reading CSV: {e}"

def get_data_points_and_bounds(df):
    """Extracts points, values, and geographic bounds from DataFrame."""
    points = df[['Longitude', 'Latitude']].values
    values = df['Value'].values
    min_lng, min_lat = points.min(axis=0)
    max_lng, max_lat = points.max(axis=0)
    return points, values, (min_lng, min_lat, max_lng, max_lat)

def interpolate_data(points, values, width, height, bounds):
    """Interpolates data onto a grid."""
    min_lng, min_lat, max_lng, max_lat = bounds
    grid_x = np.linspace(min_lng, max_lng, width)
    grid_y = np.linspace(min_lat, max_lat, height)
    grid_x_mesh, grid_y_mesh = np.meshgrid(grid_x, grid_y)
    gridded_values = griddata(points, values, (grid_x_mesh, grid_y_mesh), method='linear', fill_value=np.nan)
    return gridded_values

def create_and_save_plot(data_to_plot, output_path, width, height, extent_bounds, cmap_name='viridis', dpi=100, interpolation_method=AppConfig.DEFAULT_PLOT_INTERPOLATION):
    """Creates a plot from gridded data and saves it."""
    plt.figure(figsize=(width / 100, height / 100), dpi=dpi)
    cmap = cm.get_cmap(cmap_name)
    cmap.set_bad(color=(0, 0, 0, 0)) # Transparent for NaN
    plt.imshow(data_to_plot, origin='lower', cmap=cmap, interpolation=interpolation_method, extent=extent_bounds)
    plt.axis('off')
    plt.gca().set_position([0, 0, 1, 1])
    plt.savefig(output_path, pad_inches=0, bbox_inches='tight', transparent=True)
    plt.close()

# --- Core Raster Generation Logic ---

def generate_raster_image(input_csv_path, output_image_path, width_pixels, height_pixels, value_col_name='Value', min_threshold=None, max_threshold=None, dpi=AppConfig.RASTER_DPI, interpolation_method=AppConfig.DEFAULT_PLOT_INTERPOLATION):
    """
    Generic function to read CSV, (optionally) clip values, interpolate, and generate a raster image.
    Returns geographic bounds, (optionally) raw changes, and an error message.
    """
    df, error = load_and_validate_data(input_csv_path, AppConfig.REQUIRED_COLUMNS)
    if error:
        # Return (None, [], error) for preview context, (None, None, error) for main raster context
        return None, [] if min_threshold is not None and max_threshold is not None else None, error

    points, values, bounds = get_data_points_and_bounds(df)
    processed_values = values
    raw_changes_list = []

    if min_threshold is not None and max_threshold is not None:
        original_values_for_clipping = df[value_col_name].values
        processed_values = np.clip(original_values_for_clipping, min_threshold, max_threshold)
        changed_indices = np.where(original_values_for_clipping != processed_values)[0]
        raw_changes_list = [
            {'index': int(idx), 'original': float(original_values_for_clipping[idx]), 'clipped': float(processed_values[idx])}
            for idx in changed_indices
        ]

    try:
        gridded_values = interpolate_data(points, processed_values, width_pixels, height_pixels, bounds)
        create_and_save_plot(gridded_values, output_image_path, width_pixels, height_pixels, bounds, dpi=dpi, interpolation_method=interpolation_method)
        if min_threshold is not None and max_threshold is not None: # In preview context
            return bounds, raw_changes_list, None
        return bounds, None # In main raster context
    except Exception as e:
        err_msg = f"An error occurred during raster processing: {e}"
        if min_threshold is not None and max_threshold is not None:
            return None, [], err_msg
        return None, err_msg 