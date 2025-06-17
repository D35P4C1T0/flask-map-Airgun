#!/usr/bin/env python3
"""
Simple Heatmap Integration Example

This is the simplest way to add the heatmap functionality to your existing Flask application.
Just register the blueprint and you're ready to go!
"""

from flask import Flask
from heatmap_blueprint import register_heatmap

# Create your Flask app
app = Flask(__name__)

# Your existing routes
@app.route('/')
def home():
    return '''
    <h1>My Application</h1>
    <p>Welcome to my app!</p>
    <p><a href="/heatmap/">View Heatmap</a></p>
    '''

# Register the heatmap blueprint - that's it!
register_heatmap(app, csv_file='data/data.csv')

if __name__ == '__main__':
    print("Starting application...")
    print("Main app: http://localhost:5000/")
    print("Heatmap: http://localhost:5000/heatmap/")
    app.run(debug=True) 