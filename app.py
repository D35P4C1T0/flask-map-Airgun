import os
import json
import pandas as pd
import numpy as np
from flask import Flask, jsonify, send_from_directory, render_template, request
from flask_cors import CORS
from flask_compress import Compress
from utils.color_utils import load_colors
from config import AppConfig

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Compress communication between client and server
Compress(app)

# Configure Flask to minify JSON responses
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.json.compact = True  # For Flask 2.2+

@app.route('/')
def index():
    return render_template('index.html', config=AppConfig)

@app.route('/propagation')
def propagation():
    return render_template('propagation.html', config=AppConfig)

@app.route('/data')
def get_data():
    try:
        # Read CSV file (skip the first column which is an index)
        df = pd.read_csv('data/data.csv', index_col=0)
        
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

@app.route('/propagation-data')
def get_propagation_data():
    try:
        # Read CSV file (skip the first column which is an index)
        df = pd.read_csv('data/data.csv', index_col=0)
        print(f"Loading propagation data: {len(df)} points")
        
        # Check if we have the required columns
        required_cols = ['Latitude', 'Longitude', 'Value']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Remove any rows with NaN values
        df_clean = df.dropna(subset=required_cols)
        
        if len(df_clean) == 0:
            raise ValueError("No valid data points found after removing NaN values")
        
        # Sample the data to make it manageable
        sample_factor = max(1, len(df_clean) // 2000)  # Limit to ~2000 points for better performance
        df_sampled = df_clean.iloc[::sample_factor].copy().reset_index(drop=True)
        print(f"Processing {len(df_sampled)} sampled points")
        
        if len(df_sampled) == 0:
            raise ValueError("No data points after sampling")
        
        # Calculate center point (simple geographic center)
        try:
            center_lat = float(df_sampled['Latitude'].mean())
            center_lon = float(df_sampled['Longitude'].mean())
            
            if not (np.isfinite(center_lat) and np.isfinite(center_lon)):
                raise ValueError("Invalid center coordinates calculated")
                
        except Exception as e:
            raise ValueError(f"Error calculating center point: {str(e)}")
        
        # Calculate distances from center
        try:
            lat_diff = df_sampled['Latitude'] - center_lat
            lon_diff = df_sampled['Longitude'] - center_lon
            distances = np.sqrt(lat_diff**2 + lon_diff**2)
            
            if not np.all(np.isfinite(distances)):
                raise ValueError("Invalid distances calculated")
                
        except Exception as e:
            raise ValueError(f"Error calculating distances: {str(e)}")
        
        # Normalize noise values (0 to 1)
        try:
            min_noise = float(df_sampled['Value'].min())
            max_noise = float(df_sampled['Value'].max())
            
            if not (np.isfinite(min_noise) and np.isfinite(max_noise)):
                raise ValueError("Invalid noise values found")
            
            if max_noise == min_noise:
                # Handle case where all values are the same
                resistance = np.zeros(len(df_sampled))
            else:
                resistance = (df_sampled['Value'] - min_noise) / (max_noise - min_noise)
                
                if not np.all(np.isfinite(resistance)):
                    raise ValueError("Invalid resistance values calculated")
                    
        except Exception as e:
            raise ValueError(f"Error normalizing noise values: {str(e)}")
        
        max_distance = float(distances.max())
        if max_distance == 0 or not np.isfinite(max_distance):
            max_distance = 1.0  # Prevent division by zero
        
        # Create propagation simulation
        time_steps = 30  # Increased for smoother animation
        
        propagation_frames = []
        
        try:
            for step in range(time_steps):
                # Current time (0 to 1)
                current_time = step / max(1, time_steps - 1) if time_steps > 1 else 0
                
                # Smooth wave propagation
                normalized_distances = distances / max_distance
                
                # Smooth resistance effect
                arrival_times = normalized_distances + (resistance * 0.3)
                
                # Smooth wave front calculation
                wave_progress = current_time * 1.2  # Wave speed
                
                # Calculate smooth intensities for all points
                distance_factors = np.maximum(0, 1 - normalized_distances)
                resistance_factors = np.maximum(0.2, 1 - resistance * 0.8)
                
                # Smooth wave intensity based on distance from wave front
                wave_front_distance = np.abs(normalized_distances - wave_progress)
                wave_intensity = np.exp(-wave_front_distance * 8)  # Sharp wave front
                
                # Combine factors for smooth propagation
                base_intensity = distance_factors * resistance_factors * wave_intensity
                
                # Add subtle wave oscillation for realism
                wave_phase = (current_time * 4 - normalized_distances * 2) * np.pi
                wave_modulation = 1 + 0.1 * np.sin(wave_phase)
                
                intensities = base_intensity * wave_modulation
                
                # Filter for meaningful points with smooth threshold
                meaningful_mask = intensities > 0.05
                
                if not np.any(meaningful_mask):
                    propagation_frames.append([])
                    continue
                
                # Create smooth frame data
                meaningful_indices = np.where(meaningful_mask)[0]
                
                frame_data = []
                for idx in meaningful_indices:
                    try:
                        lat_val = float(df_sampled.iloc[idx]['Latitude'])
                        lon_val = float(df_sampled.iloc[idx]['Longitude'])
                        intensity_val = float(intensities[idx])
                        noise_val = float(df_sampled.iloc[idx]['Value'])
                        distance_val = float(distances[idx])
                        
                        # Validate all values are finite
                        if all(np.isfinite([lat_val, lon_val, intensity_val, noise_val, distance_val])):
                            frame_data.append({
                                'latitude': lat_val,
                                'longitude': lon_val,
                                'intensity': intensity_val,
                                'noise': noise_val,
                                'distance': distance_val
                            })
                    except Exception as e:
                        print(f"Warning: Skipping invalid data point at index {idx}: {e}")
                        continue
                
                propagation_frames.append(frame_data)
                
        except Exception as e:
            raise ValueError(f"Error during propagation simulation: {str(e)}")
        
        response_data = {
            'frames': propagation_frames,
            'center': {'latitude': center_lat, 'longitude': center_lon},
            'maxDistance': max_distance,
            'timeSteps': time_steps,
            'valueRange': {
                'min': min_noise,
                'max': max_noise
            },
            'sampleInfo': {
                'originalPoints': len(df),
                'sampledPoints': len(df_sampled),
                'sampleFactor': sample_factor
            }
        }
        
        print(f"Propagation calculation completed successfully with {len(propagation_frames)} frames")
        return jsonify(response_data)
        
    except Exception as e:
        error_message = str(e) if str(e) else "Unknown error occurred"
        print(f"Error in propagation calculation: {error_message}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f"Propagation calculation failed: {error_message}"}), 500

@app.route('/test-data')
def test_data():
    try:
        df = pd.read_csv('data/data.csv', index_col=0)
        return jsonify({
            'success': True,
            'rows': len(df),
            'columns': df.columns.tolist(),
            'sample': df.head(3).to_dict('records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
