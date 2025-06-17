#!/usr/bin/env python3
"""
Screenshot Feature Demo

This example demonstrates the new screenshot functionality in both the 
interactive heatmap and sound propagation visualizations.
"""

from flask import Flask
from heatmap_blueprint import register_heatmap

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Screenshot Feature Demo</h1>
    <p>This demo showcases the new screenshot functionality!</p>
    
    <h2>🎯 How to Use Screenshots:</h2>
    <ul>
        <li><strong>Interactive Heatmap:</strong> <a href="/heatmap/">Visit Heatmap</a></li>
        <li><strong>Sound Propagation:</strong> <a href="/heatmap/propagation">Visit Propagation</a></li>
    </ul>
    
    <h2>📸 Screenshot Methods:</h2>
    <ul>
        <li><strong>Button:</strong> Click the orange "Screenshot" button</li>
        <li><strong>Keyboard:</strong> Press the "S" key</li>
    </ul>
    
    <h2>✨ Features:</h2>
    <ul>
        <li>📄 <strong>Smart Filenames:</strong> Includes dataset name, timestamp, and context</li>
        <li>🏷️ <strong>Watermarks:</strong> Automatic metadata overlay</li>
        <li>🎨 <strong>High Quality:</strong> PNG format with 90% quality</li>
        <li>⚡ <strong>Instant Download:</strong> No server processing needed</li>
    </ul>
    
    <h2>📁 Example Filenames:</h2>
    <ul>
        <li><code>heatmap_Primary_Dataset_2024-01-15T14-30-25.png</code></li>
        <li><code>propagation_Secondary_Dataset_3.45s_2024-01-15T14-31-10.png</code></li>
    </ul>
    
    <p><em>Screenshots capture the current view including all visualizations, overlays, and data!</em></p>
    '''

# Configure with multiple datasets for demo
csv_files = {
    'Primary Dataset': 'data/data.csv',
    'Secondary Dataset': 'data/data2.csv', 
    'Third Dataset': 'data/data3.csv'
}

register_heatmap(app, csv_files=csv_files, default_csv='Primary Dataset')

if __name__ == '__main__':
    print("Screenshot Feature Demo")
    print("=" * 30)
    print()
    print("🎯 Features to test:")
    print("  • Heatmap screenshots with watermarks")
    print("  • Propagation screenshots with time info")
    print("  • Keyboard shortcuts (S key)")
    print("  • Smart filename generation")
    print("  • Multiple dataset support")
    print()
    print("📸 Screenshot locations:")
    print("  Heatmap: http://localhost:5000/heatmap/")
    print("  Propagation: http://localhost:5000/heatmap/propagation")
    print()
    print("🎮 Controls:")
    print("  • Click orange 'Screenshot' button")
    print("  • Press 'S' key for quick screenshot")
    print("  • Switch datasets and capture different views")
    
    app.run(debug=True) 