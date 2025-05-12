import os
import json
import pandas as pd
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure Flask to minify JSON responses
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.json.compact = True  # For Flask 2.2+

def load_colors():
    try:
        with open('colors/colors.min.json', 'r') as f:
            colors = json.load(f)
            print(f"Loaded {len(colors)} color stops")
            return colors
    except Exception as e:
        print(f"Error loading colors: {e}")
        # Try loading the original file as fallback
        try:
            with open('colors/colors.json', 'r') as f:
                colors = json.load(f)
                print(f"Loaded {len(colors)} color stops from fallback file")
                return colors
        except Exception as e2:
            print(f"Error loading fallback colors: {e2}")
            return [[0, "#80D6EA"], [1, "#8B0000"]]  # Default fallback colors

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/data')
def get_data():
    try:
        # Read CSV file
        df = pd.read_csv('data.csv')
        
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
