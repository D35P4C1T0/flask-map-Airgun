#!/usr/bin/env python3
"""
Advanced Configuration Example

This example demonstrates all available configuration options for the heatmap blueprint,
including custom settings, multiple instances, and advanced features.
"""

from flask import Flask
from heatmap_blueprint import create_heatmap_blueprint

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Advanced Heatmap Configuration</h1>
    <p>This example shows advanced configuration options.</p>
    <ul>
        <li><a href="/noise/">Noise Analysis</a> - Custom configured heatmap</li>
        <li><a href="/environmental/">Environmental Data</a> - Second heatmap instance</li>
    </ul>
    '''

# Example 1: Advanced configuration with custom settings
noise_config = {
    'CSV_FILES': {
        'Baseline Measurements': 'data/data.csv',
        'Peak Activity': 'data/data2.csv',
        'Quiet Period': 'data/data3.csv'
    },
    'DEFAULT_CSV': 'Baseline Measurements',
    'HEATMAP_RADIUS': 25,
    'HEATMAP_INTENSITY': 2.0,
    'HEATMAP_THRESHOLD': 0.1,
    'HEATMAP_OPACITY': 0.8,
    'MAP_CENTER_LAT': 25.0,
    'MAP_CENTER_LON': -58.5,
    'MAP_ZOOM': 6,
    'COLOR_SCALE': 'viridis',  # Custom color scheme
    'TITLE': 'Noise Level Analysis'
}

# Create and register first heatmap blueprint
noise_blueprint = create_heatmap_blueprint(
    config=noise_config,
    blueprint_name='noise_heatmap'
)
app.register_blueprint(noise_blueprint, url_prefix='/noise')

# Example 2: Second instance with different configuration
env_config = {
    'CSV_FILES': [
        'data/data.csv',
        'data/data2.csv'
    ],  # List format also supported
    'DEFAULT_CSV': 'data/data.csv',
    'HEATMAP_RADIUS': 15,
    'HEATMAP_INTENSITY': 1.5,
    'TITLE': 'Environmental Monitoring'
}

# Create second heatmap instance
env_blueprint = create_heatmap_blueprint(
    config=env_config,
    blueprint_name='env_heatmap'
)
app.register_blueprint(env_blueprint, url_prefix='/environmental')

# Example 3: Runtime configuration changes
@app.route('/api/update-config')
def update_config():
    """Example of how you might update configuration at runtime"""
    # Access blueprint configuration
    noise_bp_config = noise_blueprint.config
    
    # Update settings (in a real app, you'd get these from request params)
    noise_bp_config['HEATMAP_RADIUS'] = 30
    noise_bp_config['HEATMAP_INTENSITY'] = 2.5
    
    return {
        'message': 'Configuration updated',
        'new_radius': noise_bp_config['HEATMAP_RADIUS'],
        'new_intensity': noise_bp_config['HEATMAP_INTENSITY']
    }

if __name__ == '__main__':
    print("Advanced Heatmap Configuration Example")
    print("=" * 50)
    print()
    print("Instance 1 - Noise Analysis:")
    print("  URL: http://localhost:5000/noise/")
    print("  Datasets:", len(noise_config['CSV_FILES']))
    print("  Radius:", noise_config['HEATMAP_RADIUS'])
    print("  Intensity:", noise_config['HEATMAP_INTENSITY'])
    print()
    print("Instance 2 - Environmental:")
    print("  URL: http://localhost:5000/environmental/")
    print("  Datasets:", len(env_config['CSV_FILES']))
    print("  Radius:", env_config['HEATMAP_RADIUS'])
    print("  Intensity:", env_config['HEATMAP_INTENSITY'])
    print()
    print("Features demonstrated:")
    print("  ✓ Multiple heatmap instances")
    print("  ✓ Custom configuration per instance")
    print("  ✓ Different URL prefixes")
    print("  ✓ Runtime configuration updates")
    print("  ✓ Both dict and list CSV formats")
    
    app.run(debug=True) 