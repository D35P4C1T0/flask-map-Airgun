#!/usr/bin/env python3
"""
Unified Configuration System Example

This example demonstrates how the merged configuration system works:
1. Global defaults from config.json (via AppConfig)
2. Runtime overrides via register_heatmap() parameters
3. Multiple instances with different configurations

Configuration Priority (highest to lowest):
1. Runtime parameters in register_heatmap()
2. Global config.json/AppConfig defaults
3. Hardcoded fallback defaults
"""

from flask import Flask
from heatmap_blueprint import register_heatmap
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Unified Configuration System Demo</h1>
    <h2>Three Different Heatmap Instances:</h2>
    <ul>
        <li><a href="/global/">Global Config</a> - Uses config.json defaults</li>
        <li><a href="/custom/">Custom Config</a> - Runtime overrides</li>
        <li><a href="/mixed/">Mixed Config</a> - Partial overrides</li>
    </ul>
    
    <h2>Configuration Information:</h2>
    <ul>
        <li><a href="/global/config-info">Global Config Info</a> (JSON)</li>
        <li><a href="/custom/config-info">Custom Config Info</a> (JSON)</li>
        <li><a href="/mixed/config-info">Mixed Config Info</a> (JSON)</li>
    </ul>
    
    <h2>Current config.json:</h2>
    <pre id="config-content">Loading...</pre>
    
    <script>
    fetch('/api/show-config')
        .then(r => r.json())
        .then(data => {
            document.getElementById('config-content').textContent = JSON.stringify(data, null, 2);
        });
    </script>
    '''

@app.route('/api/show-config')
def show_config():
    """Show current config.json contents"""
    try:
        with open('config.json', 'r') as f:
            config_data = json.load(f)
        return {
            'status': 'loaded',
            'source': 'config.json',
            'config': config_data
        }
    except FileNotFoundError:
        return {
            'status': 'not_found',
            'message': 'config.json not found',
            'config': None
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'config': None
        }

# =================================================================
# Instance 1: Pure Global Configuration
# Uses ALL defaults from config.json (no runtime overrides)
# =================================================================

print("Creating Instance 1: Pure Global Configuration")
global_blueprint = register_heatmap(
    app,
    # No parameters = uses pure global config.json defaults
    url_prefix='/global',
    blueprint_name='global_config_heatmap'
)

# =================================================================
# Instance 2: Custom Configuration  
# Overrides most settings with runtime parameters
# =================================================================

print("Creating Instance 2: Custom Configuration with Runtime Overrides")
custom_blueprint = register_heatmap(
    app,
    # Override multiple settings
    CSV_FILES={
        'Custom Dataset A': 'data/data.csv',
        'Custom Dataset B': 'data/data2.csv',
        'Custom Dataset C': 'data/data3.csv'
    },
    DEFAULT_CSV='Custom Dataset A',
    INITIAL_HEATMAP_RADIUS=60,           # Override global default
    INITIAL_HEATMAP_INTENSITY=2.0,      # Override global default
    DEFAULT_MAP_OPACITY=0.9,            # Override global default
    REQUIRED_COLUMNS=['Latitude', 'Longitude', 'Value'],  # Same as global
    url_prefix='/custom',
    blueprint_name='custom_config_heatmap'
)

# =================================================================
# Instance 3: Mixed Configuration
# Some runtime overrides + some global defaults
# =================================================================

print("Creating Instance 3: Mixed Configuration (partial overrides)")
mixed_blueprint = register_heatmap(
    app,
    # Override only specific settings, inherit others from global config
    CSV_FILES=['data/data.csv', 'data/data2.csv'],  # Override: list format
    INITIAL_HEATMAP_RADIUS=35,                      # Override: smaller radius
    # INITIAL_HEATMAP_INTENSITY → uses global default
    # DEFAULT_MAP_OPACITY → uses global default  
    # REQUIRED_COLUMNS → uses global default
    url_prefix='/mixed',
    blueprint_name='mixed_config_heatmap'
)

# =================================================================
# Configuration Information Routes
# =================================================================

@app.route('/config-comparison')
def config_comparison():
    """Compare configurations across all instances"""
    try:
        # Get config info from each blueprint
        global_info = global_blueprint.config.get_config_info()
        custom_info = custom_blueprint.config.get_config_info()
        mixed_info = mixed_blueprint.config.get_config_info()
        
        return {
            'instances': {
                'global': {
                    'name': 'Pure Global Config',
                    'url': '/global/',
                    'info': global_info
                },
                'custom': {
                    'name': 'Custom Runtime Config',
                    'url': '/custom/',
                    'info': custom_info
                },
                'mixed': {
                    'name': 'Mixed Config',
                    'url': '/mixed/',
                    'info': mixed_info
                }
            },
            'comparison': {
                'radius': {
                    'global': global_info['current_values']['INITIAL_HEATMAP_RADIUS'],
                    'custom': custom_info['current_values']['INITIAL_HEATMAP_RADIUS'],
                    'mixed': mixed_info['current_values']['INITIAL_HEATMAP_RADIUS']
                },
                'intensity': {
                    'global': global_info['current_values']['INITIAL_HEATMAP_INTENSITY'],
                    'custom': custom_info['current_values']['INITIAL_HEATMAP_INTENSITY'],
                    'mixed': mixed_info['current_values']['INITIAL_HEATMAP_INTENSITY']
                },
                'opacity': {
                    'global': global_info['current_values']['DEFAULT_MAP_OPACITY'],
                    'custom': custom_info['current_values']['DEFAULT_MAP_OPACITY'],
                    'mixed': mixed_info['current_values']['DEFAULT_MAP_OPACITY']
                }
            }
        }
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/update-global-config', methods=['POST'])
def update_global_config():
    """
    Example of updating global config at runtime.
    In a real application, you might want to restart to reload config.json
    """
    try:
        # This is just a demonstration - config.json changes require restart
        return {
            'message': 'To change global config, edit config.json and restart the application',
            'current_config_file': 'config.json',
            'note': 'Runtime parameter changes take effect immediately per blueprint instance'
        }
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("UNIFIED CONFIGURATION SYSTEM DEMO")
    print("="*60)
    print()
    print("Configuration Priority:")
    print("  1. Runtime parameters (highest)")
    print("  2. Global config.json defaults")  
    print("  3. Hardcoded fallbacks (lowest)")
    print()
    print("Instances created:")
    print("  /global/     → Pure global config (no overrides)")
    print("  /custom/     → Heavy runtime overrides")
    print("  /mixed/      → Partial runtime overrides")
    print()
    print("Configuration Info:")
    print("  /config-comparison → Compare all instances")
    print("  /<instance>/config-info → Individual config details")
    print()
    print("To test the system:")
    print("  1. Edit config.json to change global defaults")
    print("  2. Restart this script")
    print("  3. Compare configurations between instances")
    print("  4. See how global changes affect each instance differently")
    print()
    print("="*60)
    
    app.run(debug=True) 