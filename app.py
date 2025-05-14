import os
import json
import pandas as pd
from flask import Flask, jsonify, send_from_directory, render_template
from flask_cors import CORS
from utils.color_utils import load_colors
from config import AppConfig

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure Flask to minify JSON responses
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.json.compact = True  # For Flask 2.2+

@app.route('/')
def index():
    return render_template('index.html', config=AppConfig)

@app.route('/data')
def get_data():
    try:
        # Read CSV file
        df = pd.read_csv('data/data.csv')
        
        # Extract required columns
        data = df[['Latitude', 'Longitude', 'Value']].to_dict(orient='records')
        
        # Calculate data range for the heatmap
        min_val = float(df['Value'].min())
        max_val = float(df['Value'].max())
        value_range = {
            'min': min_val,
            'max': max_val
        }
        
        print(f"Data range: min={min_val}, max={max_val}")
        print(f"Sample values: {df['Value'].head().tolist()}")
        
        # Load color configuration
        colors = load_colors()
        
        response_data = {
            'data': data,
            'valueRange': value_range,
            'colorScale': colors
        }
        
        return jsonify(response_data)
    except Exception as e:
        print(f"Error in get_data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
