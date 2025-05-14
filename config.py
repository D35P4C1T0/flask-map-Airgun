import os

# --- App Configuration ---
class AppConfig:
    INPUT_CSV_FILE = 'data/data.csv'
    STATIC_FOLDER = 'static'
    # OUTPUT_RASTER_IMAGE_FILENAME = 'output_raster.png'
    # PREVIEW_RASTER_IMAGE_FILENAME = 'preview_raster.png'
    FRONTEND_TEMPLATE = 'index.html'
    REQUIRED_COLUMNS = ['Latitude', 'Longitude', 'Value']

    # Opacity setting for map layer
    DEFAULT_MAP_OPACITY = 0.75

    # Initial UI values for heatmap layer controls
    INITIAL_HEATMAP_RADIUS = 40
    INITIAL_HEATMAP_INTENSITY = 1.5 # Make it a float for consistency with step
    INITIAL_HEATMAP_THRESHOLD = 0.00

    @staticmethod
    def get_output_raster_path():
        return os.path.join(AppConfig.STATIC_FOLDER, AppConfig.OUTPUT_RASTER_IMAGE_FILENAME)

    @staticmethod
    def get_preview_raster_path():
        return os.path.join(AppConfig.STATIC_FOLDER, AppConfig.PREVIEW_RASTER_IMAGE_FILENAME)

if not os.path.exists(AppConfig.STATIC_FOLDER):
    os.makedirs(AppConfig.STATIC_FOLDER) 