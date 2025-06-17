"""
Flask App Integration Example
How to configure multiple CSV files in your existing Flask application
"""

from flask import Flask, render_template, request, redirect, url_for
from heatmap_blueprint import register_heatmap
import os
import glob

# Your existing Flask application
app = Flask(__name__)
app.secret_key = 'your-secret-key'

# ====================================================================
# Method 1: Static Configuration (Hardcoded CSV Files)
# ====================================================================

def setup_static_csv_files():
    """
    Simplest method: Define your CSV files directly in code
    """
    
    # Define your CSV files with custom names
    noise_map_files = {
        'Morning Survey (7-9 AM)': 'data/surveys/morning_survey.csv',
        'Afternoon Survey (12-2 PM)': 'data/surveys/afternoon_survey.csv',
        'Evening Survey (6-8 PM)': 'data/surveys/evening_survey.csv',
        'Night Survey (10-12 PM)': 'data/surveys/night_survey.csv',
        'Weekend Baseline': 'data/surveys/weekend_baseline.csv'
    }
    
    register_heatmap(app,
        CSV_FILES=noise_map_files,
        DEFAULT_CSV='Morning Survey (7-9 AM)',
        URL_PREFIX='/noise-maps',
        BLUEPRINT_NAME='noise_analysis',
        INITIAL_HEATMAP_RADIUS=45,
        INITIAL_HEATMAP_INTENSITY=1.8
    )

# ====================================================================
# Method 2: Dynamic Discovery (Auto-find CSV files)
# ====================================================================

def setup_dynamic_csv_discovery():
    """
    Automatically discover CSV files in a directory
    """
    
    # Automatically find all CSV files in your data directory
    data_directory = 'data/noise_surveys'
    csv_pattern = os.path.join(data_directory, '*.csv')
    csv_files = glob.glob(csv_pattern)
    
    # Create a dictionary with nice display names
    noise_map_files = {}
    for csv_file in csv_files:
        # Extract filename without extension for display name
        filename = os.path.basename(csv_file)
        display_name = filename.replace('.csv', '').replace('_', ' ').title()
        noise_map_files[display_name] = csv_file
    
    print(f"Found CSV files: {list(noise_map_files.keys())}")
    
    if noise_map_files:  # Only register if we found files
        register_heatmap(app,
            CSV_FILES=noise_map_files,
            DEFAULT_CSV=list(noise_map_files.keys())[0],  # First file as default
            URL_PREFIX='/auto-discovered-maps',
            BLUEPRINT_NAME='auto_discovery_maps'
        )

# ====================================================================
# Method 3: Configuration from Database/API
# ====================================================================

def get_csv_files_from_database():
    """
    Simulate getting CSV file list from a database
    In real app, this would query your database
    """
    # This could be replaced with actual database queries
    # For example: SELECT name, filepath FROM survey_files WHERE active=1
    
    database_files = [
        {'name': 'Latest Airgun Survey', 'path': 'data/generated/latest_airgun.csv'},
        {'name': 'Processed Results Q1', 'path': 'data/processed/q1_results.csv'},
        {'name': 'Processed Results Q2', 'path': 'data/processed/q2_results.csv'},
        {'name': 'Baseline Comparison', 'path': 'data/baseline/comparison.csv'}
    ]
    
    return {item['name']: item['path'] for item in database_files}

def setup_database_driven_csv():
    """
    Get CSV files from database or API
    """
    
    csv_files = get_csv_files_from_database()
    
    register_heatmap(app,
        CSV_FILES=csv_files,
        DEFAULT_CSV='Latest Airgun Survey',
        URL_PREFIX='/database-maps',
        BLUEPRINT_NAME='database_driven_maps'
    )

# ====================================================================
# Method 4: User-Configurable CSV Files
# ====================================================================

# Global variable to store user-configured CSV files
user_csv_files = {
    'Default Survey': 'data/data.csv'  # Start with default
}

def setup_user_configurable_csv():
    """
    Allow users to add/remove CSV files through web interface
    """
    
    register_heatmap(app,
        CSV_FILES=user_csv_files,
        DEFAULT_CSV='Default Survey',
        URL_PREFIX='/user-maps',
        BLUEPRINT_NAME='user_configurable_maps'
    )

# ====================================================================
# Method 5: Environment-Based Configuration
# ====================================================================

def setup_environment_based_csv():
    """
    Configure CSV files based on environment or config file
    """
    
    # You could read this from environment variables, config file, etc.
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        csv_files = {
            'Production Survey A': 'data/production/survey_a.csv',
            'Production Survey B': 'data/production/survey_b.csv'
        }
    else:
        csv_files = {
            'Test Survey 1': 'data/test/test_survey_1.csv',
            'Test Survey 2': 'data/test/test_survey_2.csv',
            'Debug Data': 'data/debug/debug_data.csv'
        }
    
    register_heatmap(app,
        CSV_FILES=csv_files,
        DEFAULT_CSV=list(csv_files.keys())[0],
        URL_PREFIX='/env-maps',
        BLUEPRINT_NAME='environment_maps'
    )

# ====================================================================
# Your Existing Flask Routes
# ====================================================================

@app.route('/')
def home():
    return """
    <h1>My Flask Application with Integrated Heatmaps</h1>
    <h2>Available Noise Map Visualizations:</h2>
    <ul>
        <li><a href="/noise-maps/">Static Configuration Maps</a></li>
        <li><a href="/auto-discovered-maps/">Auto-Discovered Maps</a></li>
        <li><a href="/database-maps/">Database-Driven Maps</a></li>
        <li><a href="/user-maps/">User-Configurable Maps</a></li>
        <li><a href="/env-maps/">Environment-Based Maps</a></li>
    </ul>
    
    <h2>Admin Functions:</h2>
    <ul>
        <li><a href="/admin/csv-manager">Manage CSV Files</a></li>
        <li><a href="/admin/refresh-files">Refresh File List</a></li>
    </ul>
    """

@app.route('/admin/csv-manager')
def csv_manager():
    return f"""
    <h1>CSV File Manager</h1>
    <h2>Currently Available Files:</h2>
    <ul>
        {''.join([f'<li><strong>{name}</strong>: {path}</li>' for name, path in user_csv_files.items()])}
    </ul>
    
    <h3>Add New CSV File:</h3>
    <form action="/admin/add-csv" method="post">
        <label>Display Name: <input type="text" name="name" placeholder="My Survey" required></label><br><br>
        <label>File Path: <input type="text" name="path" placeholder="data/my_survey.csv" required></label><br><br>
        <button type="submit">Add CSV File</button>
    </form>
    
    <p><a href="/">Back to Home</a></p>
    """

@app.route('/admin/add-csv', methods=['POST'])
def add_csv_file():
    """Add a new CSV file to the user-configurable list"""
    name = request.form.get('name')
    path = request.form.get('path')
    
    if name and path:
        user_csv_files[name] = path
        return f"<h2>Added CSV file: {name}</h2><p><a href='/admin/csv-manager'>Back to Manager</a></p>"
    else:
        return "<h2>Error: Name and path required</h2><p><a href='/admin/csv-manager'>Back to Manager</a></p>"

@app.route('/admin/refresh-files')
def refresh_files():
    """Refresh the auto-discovered files"""
    # This would re-scan directories, refresh database, etc.
    return "<h2>File list refreshed!</h2><p><a href='/'>Back to Home</a></p>"

# ====================================================================
# Practical Example: Your Actual Use Case
# ====================================================================

def setup_your_noise_survey_files():
    """
    Example configuration for your specific noise survey use case
    """
    
    # Your actual CSV files - modify these paths to match your setup
    your_csv_files = {
        # Time-based surveys
        'Morning Survey (6-9 AM)': 'data/time_based/morning_survey.csv',
        'Midday Survey (11-2 PM)': 'data/time_based/midday_survey.csv',
        'Evening Survey (5-8 PM)': 'data/time_based/evening_survey.csv',
        'Night Survey (10-1 AM)': 'data/time_based/night_survey.csv',
        
        # Location-based surveys
        'Northern Sector': 'data/sectors/north_sector.csv',
        'Southern Sector': 'data/sectors/south_sector.csv',
        'Eastern Sector': 'data/sectors/east_sector.csv',
        'Western Sector': 'data/sectors/west_sector.csv',
        
        # Equipment-based surveys
        'Airgun Array 1': 'data/equipment/airgun_array_1.csv',
        'Airgun Array 2': 'data/equipment/airgun_array_2.csv',
        'Airgun Array 3': 'data/equipment/airgun_array_3.csv',
        
        # Baseline and comparisons
        'Environmental Baseline': 'data/baseline/environmental_baseline.csv',
        'Pre-Survey Baseline': 'data/baseline/pre_survey_baseline.csv',
        'Post-Survey Analysis': 'data/analysis/post_survey_analysis.csv'
    }
    
    register_heatmap(app,
        CSV_FILES=your_csv_files,
        DEFAULT_CSV='Morning Survey (6-9 AM)',
        URL_PREFIX='/survey-analysis',
        BLUEPRINT_NAME='survey_analysis',
        COLORS_DIR='colors',
        INITIAL_HEATMAP_RADIUS=50,
        INITIAL_HEATMAP_INTENSITY=1.5,
        DEFAULT_MAP_OPACITY=0.8
    )

# ====================================================================
# Application Initialization
# ====================================================================

if __name__ == '__main__':
    print("Setting up CSV file configurations...")
    
    # Choose which method(s) to use:
    
    # Method 1: Static configuration
    setup_static_csv_files()
    
    # Method 2: Auto-discovery
    # setup_dynamic_csv_discovery()  # Uncomment to use
    
    # Method 3: Database-driven
    # setup_database_driven_csv()  # Uncomment to use
    
    # Method 4: User-configurable
    setup_user_configurable_csv()
    
    # Method 5: Environment-based
    # setup_environment_based_csv()  # Uncomment to use
    
    # Your specific use case
    setup_your_noise_survey_files()
    
    print("CSV files configured successfully!")
    print("Starting Flask application...")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 