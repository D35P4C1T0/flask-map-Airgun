from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_compress import Compress
from heatmap_blueprint import register_heatmap

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Compress communication between client and server
Compress(app)

# Configure Flask to minify JSON responses
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.json.compact = True  # For Flask 2.2+

csv_files = {
    # Display Name : File Path
    'Primary Dataset': 'data/data.csv',
    'Secondary Dataset': 'data/data2.csv', 
    'Third Dataset': 'data/data3.csv'
}

# Register heatmap blueprint
heatmap_url_prefix = '/map'
register_heatmap(app,
    CSV_FILES=csv_files,
    DEFAULT_CSV='Primary Dataset',  # Use the display name, not file path
    URL_PREFIX=heatmap_url_prefix,  # Heatmap will be at /map/
    BLUEPRINT_NAME='multi_csv_heatmap'
)

@app.route('/')
def index():
    """Redirect to heatmap view"""
    from flask import redirect
    return redirect(heatmap_url_prefix + '/')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    print("Starting Flask app with multiple CSV support...")
    print("Available routes:")
    print("  / - Redirects to heatmap")
    print(f"  {heatmap_url_prefix}/ - Unified view with heatmap and propagation")
    app.run(debug=True)
