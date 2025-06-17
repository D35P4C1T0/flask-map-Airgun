"""
Integration Examples for Heatmap Blueprint

This file shows different ways to integrate the heatmap functionality
into existing Flask applications.
"""

from flask import Flask
from heatmap_blueprint import create_heatmap_blueprint, register_heatmap, HeatmapConfig

# =====================================================
# Example 1: Simple Integration with Default Settings
# =====================================================

def example_1_simple_integration():
    """
    Simplest way to add heatmap to an existing Flask app.
    Uses default configuration and URL prefix /heatmap
    """
    
    # Your existing Flask app
    app = Flask(__name__)
    
    # Your existing routes
    @app.route('/')
    def home():
        return "Welcome to my existing Flask app!"
    
    @app.route('/about')
    def about():
        return "About page of my existing app"
    
    # Add heatmap functionality with one line
    register_heatmap(app)
    
    # Now your app has heatmap routes at:
    # /heatmap/ - Main heatmap view
    # /heatmap/propagation - Propagation animation
    # /heatmap/data - Data API endpoint
    # /heatmap/propagation-data - Propagation data API
    
    return app

# =====================================================
# Example 2: Custom Configuration
# =====================================================

def example_2_custom_config():
    """
    Integration with custom configuration for file paths,
    URL prefix, and other settings.
    """
    
    app = Flask(__name__)
    
    # Your existing routes
    @app.route('/')
    def home():
        return "My custom Flask app"
    
    # Custom configuration
    custom_config = {
        'INPUT_CSV_FILE': 'my_data/noise_measurements.csv',
        'STATIC_FOLDER': 'my_static',
        'TEMPLATE_FOLDER': 'my_templates', 
        'COLORS_DIR': 'my_colors',
        'URL_PREFIX': '/noise-analysis',  # Custom URL prefix
        'BLUEPRINT_NAME': 'noise_viz',
        'INITIAL_HEATMAP_RADIUS': 60,
        'INITIAL_HEATMAP_INTENSITY': 2.0
    }
    
    register_heatmap(app, **custom_config)
    
    # Now accessible at:
    # /noise-analysis/ - Main view
    # /noise-analysis/propagation - Animation
    # etc.
    
    return app

# =====================================================
# Example 3: Multiple Heatmaps with Different Data
# =====================================================

def example_3_multiple_heatmaps():
    """
    Integration of multiple heatmap instances with different datasets.
    Useful for comparing different data sources or time periods.
    """
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return """
        <h1>Multi-Dataset Heatmap Viewer</h1>
        <ul>
            <li><a href="/airgun-data/">Airgun Noise Data</a></li>
            <li><a href="/traffic-data/">Traffic Noise Data</a></li>
            <li><a href="/construction-data/">Construction Noise Data</a></li>
        </ul>
        """
    
    # Airgun data heatmap
    airgun_config = {
        'INPUT_CSV_FILE': 'data/airgun_noise.csv',
        'URL_PREFIX': '/airgun-data',
        'BLUEPRINT_NAME': 'airgun_heatmap'
    }
    register_heatmap(app, **airgun_config)
    
    # Traffic data heatmap  
    traffic_config = {
        'INPUT_CSV_FILE': 'data/traffic_noise.csv',
        'URL_PREFIX': '/traffic-data',
        'BLUEPRINT_NAME': 'traffic_heatmap',
        'COLORS_DIR': 'colors/traffic'  # Different color scheme
    }
    register_heatmap(app, **traffic_config)
    
    # Construction data heatmap
    construction_config = {
        'INPUT_CSV_FILE': 'data/construction_noise.csv',
        'URL_PREFIX': '/construction-data',
        'BLUEPRINT_NAME': 'construction_heatmap',
        'COLORS_DIR': 'colors/construction'
    }
    register_heatmap(app, **construction_config)
    
    return app

# =====================================================
# Example 4: Advanced Integration with Blueprint Factory
# =====================================================

def example_4_advanced_integration():
    """
    Advanced integration using the blueprint factory directly
    for maximum control and customization.
    """
    
    app = Flask(__name__)
    
    # Your existing configuration
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'your-secret-key'
    
    @app.route('/')
    def dashboard():
        return """
        <h1>Environmental Monitoring Dashboard</h1>
        <ul>
            <li><a href="/analysis/">Noise Analysis</a></li>
            <li><a href="/reports/">Generate Reports</a></li>
        </ul>
        """
    
    @app.route('/reports/')
    def reports():
        return "Reports functionality"
    
    # Create custom heatmap configuration
    heatmap_config = HeatmapConfig(
        INPUT_CSV_FILE='environmental_data/noise_levels.csv',
        URL_PREFIX='/analysis',
        BLUEPRINT_NAME='environmental_analysis',
        INITIAL_HEATMAP_RADIUS=45,
        INITIAL_HEATMAP_INTENSITY=1.8,
        DEFAULT_MAP_OPACITY=0.8
    )
    
    # Create and register blueprint
    heatmap_bp = create_heatmap_blueprint(heatmap_config)
    app.register_blueprint(heatmap_bp)
    
    # You can also add custom routes to the blueprint before registration
    @heatmap_bp.route('/custom-endpoint')
    def custom_analysis():
        return "Custom analysis endpoint"
    
    return app

# =====================================================
# Example 5: Integration with Existing Authentication
# =====================================================

def example_5_with_authentication():
    """
    Integration with existing authentication system.
    Shows how to protect heatmap routes with login requirements.
    """
    
    from functools import wraps
    from flask import session, redirect, url_for
    
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'
    
    # Simple authentication decorator (replace with your auth system)
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    
    @app.route('/')
    def home():
        return '<a href="/login">Login</a> or <a href="/heatmap/">View Heatmap</a>'
    
    @app.route('/login')
    def login():
        session['user_id'] = 'demo_user'  # Simplified login
        return redirect(url_for('heatmap.index'))
    
    # Create heatmap blueprint
    heatmap_bp = create_heatmap_blueprint()
    
    # Add authentication to all heatmap routes
    @heatmap_bp.before_request
    def require_login():
        if 'user_id' not in session:
            return redirect(url_for('login'))
    
    app.register_blueprint(heatmap_bp)
    
    return app

# =====================================================
# Example 6: Minimal Integration for Existing Large App
# =====================================================

def example_6_minimal_integration():
    """
    Minimal integration example for adding to existing large applications.
    Just adds the essential heatmap functionality without conflicts.
    """
    
    # Assume you have an existing Flask app instance
    def add_heatmap_to_existing_app(existing_app):
        """
        Function to add heatmap to any existing Flask app.
        
        Args:
            existing_app: Your existing Flask application instance
        """
        
        # Simple integration with minimal configuration
        blueprint = create_heatmap_blueprint({
            'URL_PREFIX': '/heatmap',
            'BLUEPRINT_NAME': 'heatmap_addon'
        })
        
        existing_app.register_blueprint(blueprint)
        
        return existing_app
    
    # Usage:
    # my_existing_app = add_heatmap_to_existing_app(my_existing_app)
    
    return add_heatmap_to_existing_app

# =====================================================
# Run Examples
# =====================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        
        if example_num == '1':
            app = example_1_simple_integration()
        elif example_num == '2':
            app = example_2_custom_config()
        elif example_num == '3':
            app = example_3_multiple_heatmaps()
        elif example_num == '4':
            app = example_4_advanced_integration()
        elif example_num == '5':
            app = example_5_with_authentication()
        else:
            print("Usage: python integration_examples.py [1-5]")
            sys.exit(1)
        
        print(f"Running example {example_num}")
        app.run(debug=True)
    else:
        print("Usage: python integration_examples.py [1-5]")
        print("Examples:")
        print("  1 - Simple integration")
        print("  2 - Custom configuration")
        print("  3 - Multiple heatmaps")
        print("  4 - Advanced integration")
        print("  5 - With authentication") 