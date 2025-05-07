import os
import matplotlib # Keep this for matplotlib.use('Agg')
matplotlib.use('Agg') # Must be called before pyplot import

from flask import Flask, jsonify, send_from_directory, redirect, url_for, request
from flask_cors import CORS

from config import AppConfig
from raster_utils import generate_raster_image, load_and_validate_data # Specific import for /value-range

app = Flask(__name__)
CORS(app)

# --- Global State (initialized at startup) ---
RASTER_BOUNDS = None
RASTER_GENERATION_ERROR = None

# --- Initial Raster Generation (Application Startup) ---
print(f"Generating main raster from {AppConfig.INPUT_CSV_FILE} on startup...")
RASTER_BOUNDS, RASTER_GENERATION_ERROR = generate_raster_image(
    AppConfig.INPUT_CSV_FILE,
    AppConfig.get_output_raster_path(),
    AppConfig.RASTER_WIDTH_PIXELS,
    AppConfig.RASTER_HEIGHT_PIXELS,
    dpi=AppConfig.RASTER_DPI, # Explicitly set DPI for main raster
    interpolation_method=AppConfig.DEFAULT_PLOT_INTERPOLATION # Use default interpolation
)

if RASTER_GENERATION_ERROR:
    print(f"Initial main raster generation failed: {RASTER_GENERATION_ERROR}")
else:
    print(f"Main raster image generated at {AppConfig.get_output_raster_path()}")
    print(f"Geographic bounds: {RASTER_BOUNDS}")

# --- Flask Routes ---

@app.route('/')
def index():
    return redirect(url_for('serve_static', filename=AppConfig.FRONTEND_TEMPLATE))

@app.route('/raster-info', methods=['GET'])
def get_raster_info():
    if RASTER_GENERATION_ERROR:
        return jsonify({"error": f"Raster generation failed: {RASTER_GENERATION_ERROR}"}), 500
    if RASTER_BOUNDS is None:
        return jsonify({"error": "Raster bounds not available."}), 500
    
    image_url = f'/{AppConfig.STATIC_FOLDER}/{AppConfig.OUTPUT_RASTER_IMAGE_FILENAME}'
    return jsonify({
        "imageUrl": image_url,
        "bounds": {
            "south": RASTER_BOUNDS[1], "west": RASTER_BOUNDS[0],
            "north": RASTER_BOUNDS[3], "east": RASTER_BOUNDS[2]
        },
        "defaultOpacity": AppConfig.DEFAULT_RASTER_OPACITY
    })

@app.route(f'/{AppConfig.STATIC_FOLDER}/<path:filename>')
def serve_static(filename):
    # Construct the full path to the file within the static folder
    # This is important for os.path.exists to work correctly
    # and for send_from_directory to resolve the file from the correct base directory.
    # AppConfig.STATIC_FOLDER is already the correct base directory for send_from_directory.
    file_path_to_check = os.path.join(AppConfig.STATIC_FOLDER, filename)
    if not os.path.exists(file_path_to_check):
        return "File not found", 404
    return send_from_directory(AppConfig.STATIC_FOLDER, filename)

@app.route('/value-range', methods=['GET'])
def get_value_range():
    df, error = load_and_validate_data(AppConfig.INPUT_CSV_FILE, AppConfig.REQUIRED_COLUMNS)
    if error:
        return jsonify({'error': error}), 500
    try:
        # Assuming 'Value' is the column name for data values
        vals = df['Value'].values 
        return jsonify({
            'min': float(vals.min()), 
            'max': float(vals.max()),
            'defaultOpacity': AppConfig.DEFAULT_RASTER_OPACITY
        })
    except Exception as e:
        return jsonify({'error': f"Error processing value range: {e}"}), 500

@app.route('/preview', methods=['GET'])
def preview():
    try:
        min_thr_str = request.args.get('min')
        max_thr_str = request.args.get('max')
        resolution_str = request.args.get('resolution', str(AppConfig.DEFAULT_PREVIEW_RESOLUTION))
        dpi_str = request.args.get('dpi', str(AppConfig.DEFAULT_PREVIEW_DPI))
        interpolation_str = request.args.get('interpolation', AppConfig.DEFAULT_PLOT_INTERPOLATION) # Get interpolation string

        if min_thr_str is None or max_thr_str is None:
             return jsonify({'error': 'Missing min or max threshold values'}), 400

        min_thr = float(min_thr_str)
        max_thr = float(max_thr_str)
        resolution = int(resolution_str)
        preview_dpi = int(dpi_str)
        
        resolution = max(AppConfig.MIN_PREVIEW_RESOLUTION, min(resolution, AppConfig.MAX_PREVIEW_RESOLUTION))
        preview_dpi = max(AppConfig.MIN_PREVIEW_DPI, min(preview_dpi, AppConfig.MAX_PREVIEW_DPI))

        # Validate interpolation method
        if interpolation_str not in AppConfig.PLOT_INTERPOLATION_OPTIONS:
            interpolation_method = AppConfig.DEFAULT_PLOT_INTERPOLATION # Fallback to default
        else:
            interpolation_method = interpolation_str

    except ValueError:
        return jsonify({'error': 'Invalid threshold, resolution, DPI, or interpolation values'}), 400

    bounds, raw_changes, err = generate_raster_image(
        AppConfig.INPUT_CSV_FILE,
        AppConfig.get_preview_raster_path(),
        resolution, resolution, # width, height
        min_threshold=min_thr, 
        max_threshold=max_thr,
        dpi=preview_dpi,
        interpolation_method=interpolation_method # Pass validated interpolation method
    )

    if err:
        return jsonify({'error': err}), 500
    if bounds is None:
        # This case should ideally be covered by err, but as a safeguard:
        return jsonify({'error': 'Failed to generate preview bounds (bounds is None).'}), 500

    return jsonify({
        'imageUrl': f'/{AppConfig.STATIC_FOLDER}/{AppConfig.PREVIEW_RASTER_IMAGE_FILENAME}',
        'bounds': {
            'south': bounds[1], 'west': bounds[0],
            'north': bounds[3], 'east': bounds[2]
        },
        'rawChanges': raw_changes
    })

@app.route('/tune')
def tune():
    return send_from_directory(AppConfig.STATIC_FOLDER, 'preview.html')

if __name__ == '__main__':
    app.run(debug=True)
