import os

# --- App Configuration ---
class AppConfig:
    INPUT_CSV_FILE = 'data.csv'
    STATIC_FOLDER = 'static'
    OUTPUT_RASTER_IMAGE_FILENAME = 'output_raster.png'
    PREVIEW_RASTER_IMAGE_FILENAME = 'preview_raster.png'
    FRONTEND_TEMPLATE = 'index.html'
    REQUIRED_COLUMNS = ['Latitude', 'Longitude', 'Value']
    RASTER_WIDTH_PIXELS = 6000
    RASTER_HEIGHT_PIXELS = 6000
    RASTER_DPI = 100
    # Default preview resolution, can be overridden by request arg
    DEFAULT_PREVIEW_RESOLUTION = 300 
    MIN_PREVIEW_RESOLUTION = 100
    MAX_PREVIEW_RESOLUTION = 4000

    # DPI settings for preview
    DEFAULT_PREVIEW_DPI = 100
    MIN_PREVIEW_DPI = 50
    MAX_PREVIEW_DPI = 600

    # Plotting settings
    PLOT_INTERPOLATION_OPTIONS = ['nearest', 'bilinear', 'bicubic', 'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']
    DEFAULT_PLOT_INTERPOLATION = 'nearest' # Good for preserving original data values without blurring

    # Opacity setting for raster layers
    DEFAULT_RASTER_OPACITY = 0.75

    @staticmethod
    def get_output_raster_path():
        return os.path.join(AppConfig.STATIC_FOLDER, AppConfig.OUTPUT_RASTER_IMAGE_FILENAME)

    @staticmethod
    def get_preview_raster_path():
        return os.path.join(AppConfig.STATIC_FOLDER, AppConfig.PREVIEW_RASTER_IMAGE_FILENAME)

if not os.path.exists(AppConfig.STATIC_FOLDER):
    os.makedirs(AppConfig.STATIC_FOLDER) 