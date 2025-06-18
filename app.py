import os
import json
import pandas as pd
import numpy as np
from flask import Flask, jsonify, send_from_directory, render_template, request
from flask_cors import CORS
from flask_compress import Compress
from utils.color_utils import load_colors
from config import AppConfig
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

register_heatmap(app,
    CSV_FILES=csv_files,
    DEFAULT_CSV='Primary Dataset',  # Use the display name, not file path
    URL_PREFIX='/heatmap',          # Heatmap will be at /heatmap/
    BLUEPRINT_NAME='multi_csv_heatmap'
)

@app.route('/')
def index():
    """Main page with links to different sections"""
    return app.send_static_file('index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    print("Starting Flask app with multiple CSV support...")
    print("Available routes:")
    print("  / - Main dashboard")
    print("  /heatmap/ - Multi-CSV heatmap")
    print("  /heatmap/propagation - Multi-CSV propagation")
    app.run(debug=True)
