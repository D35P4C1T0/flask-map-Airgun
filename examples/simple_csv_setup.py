"""
Simple CSV Setup Example for Your Flask App

This shows the easiest way to add multiple CSV files to your existing Flask application.
"""

from flask import Flask
from heatmap_blueprint import register_heatmap

# Your existing Flask app
app = Flask(__name__)

# ====================================================================
# SIMPLEST METHOD: Just add your CSV files here
# ====================================================================

# Define your CSV files - CHANGE THESE PATHS TO MATCH YOUR FILES
my_csv_files = {
    # Display Name : File Path
    'Current Survey': 'data/data.csv',  # Your existing file
    'Survey 2023-Q1': 'data/survey_2023_q1.csv',
    'Survey 2023-Q2': 'data/survey_2023_q2.csv', 
    'Survey 2022': 'data/survey_2022.csv',
    'Baseline Study': 'data/baseline_study.csv'
}

# Add the heatmap with multiple CSV support to your app
register_heatmap(app,
    CSV_FILES=my_csv_files,                    # Your CSV files dictionary
    DEFAULT_CSV='Current Survey',              # Which one to show first
    URL_PREFIX='/heatmap',                     # URL where heatmap appears
    BLUEPRINT_NAME='noise_heatmap'             # Unique name for this heatmap
)

# ====================================================================
# Alternative: Auto-discover CSV files in a folder
# ====================================================================

import os
import glob

def auto_discover_csv_files():
    """
    Automatically find all CSV files in your data folder
    """
    csv_files = glob.glob('data/*.csv')
    
    # Create nice display names from filenames
    csv_dict = {}
    for file_path in csv_files:
        filename = os.path.basename(file_path)
        display_name = filename.replace('.csv', '').replace('_', ' ').title()
        csv_dict[display_name] = file_path
    
    return csv_dict

# Uncomment these lines to use auto-discovery instead:
# auto_csv_files = auto_discover_csv_files()
# register_heatmap(app,
#     CSV_FILES=auto_csv_files,
#     DEFAULT_CSV=list(auto_csv_files.keys())[0] if auto_csv_files else None,
#     URL_PREFIX='/auto-heatmap',
#     BLUEPRINT_NAME='auto_heatmap'
# )

# ====================================================================
# Your existing Flask routes
# ====================================================================

@app.route('/')
def home():
    return '''
    <h1>My Flask App with Multiple CSV Heatmaps</h1>
    <p>Now you can select different CSV files from the dropdown!</p>
    <ul>
        <li><a href="/heatmap/">View Heatmap (with CSV selector)</a></li>
        <li><a href="/heatmap/propagation">View Propagation Animation</a></li>
    </ul>
    '''

if __name__ == '__main__':
    print("Starting Flask app with multiple CSV support...")
    app.run(debug=True) 