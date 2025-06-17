#!/usr/bin/env python3
"""
Multiple CSV Files with Dropdown Example

This example shows how to configure the heatmap to work with multiple CSV files
and provide a dropdown selector for users to switch between datasets.
"""

from flask import Flask
from heatmap_blueprint import register_heatmap

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Multi-Dataset Heatmap Application</h1>
    <p>This application demonstrates multiple CSV file support with dropdown selection.</p>
    <ul>
        <li><a href="/heatmap/">Interactive Heatmap</a> - Switch between datasets using the dropdown</li>
        <li><a href="/heatmap/propagation">Sound Propagation</a> - Animated visualization</li>
    </ul>
    '''

# Configure multiple CSV files
csv_files = {
    'Primary Dataset': 'data/data.csv',
    'Secondary Dataset': 'data/data2.csv', 
    'Third Dataset': 'data/data3.csv'
}

# Register heatmap with multiple CSV support
register_heatmap(
    app=app,
    csv_files=csv_files,  # Pass dictionary of CSV files
    default_csv='Primary Dataset',  # Set default selection
    url_prefix='/heatmap',  # Custom URL prefix
    blueprint_name='heatmap'  # Custom blueprint name
)

if __name__ == '__main__':
    print("Multi-CSV Heatmap Application")
    print("=" * 40)
    print("Available datasets:")
    for name, file in csv_files.items():
        print(f"  - {name}: {file}")
    print()
    print("URLs:")
    print("  Main app: http://localhost:5000/")
    print("  Heatmap: http://localhost:5000/heatmap/")
    print("  Propagation: http://localhost:5000/heatmap/propagation")
    print()
    print("Features:")
    print("  ✓ Dropdown selector for switching datasets")
    print("  ✓ Real-time map updates")
    print("  ✓ Independent configurations per dataset")
    
    app.run(debug=True) 