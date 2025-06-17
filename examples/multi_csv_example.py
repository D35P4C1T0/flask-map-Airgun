"""
Multi-CSV Heatmap Example

This example demonstrates how to use the enhanced heatmap blueprint
with multiple CSV files that can be selected dynamically.
"""

from flask import Flask
from heatmap_blueprint import register_heatmap, create_heatmap_blueprint, HeatmapConfig

# ====================================================================
# Example 1: Simple Multiple CSV Files (List Format)
# ====================================================================

def example_list_format():
    """
    Example using a list of CSV file paths.
    Display names will be automatically generated from filenames.
    """
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return """
        <h1>Multi-CSV Heatmap Example</h1>
        <p>This example shows multiple CSV files that can be selected dynamically.</p>
        <ul>
            <li><a href="/heatmap/">View Heatmap with CSV Selector</a></li>
            <li><a href="/heatmap/propagation">View Propagation Animation</a></li>
        </ul>
        """
    
    # Configure multiple CSV files as a list
    csv_files = [
        'data/airgun_survey_2023.csv',
        'data/airgun_survey_2022.csv', 
        'data/airgun_survey_2021.csv',
        'data/baseline_noise.csv'
    ]
    
    register_heatmap(app,
        CSV_FILES=csv_files,  # List of CSV files
        DEFAULT_CSV='airgun_survey_2023',  # Default selection (filename without extension)
        URL_PREFIX='/heatmap',
        BLUEPRINT_NAME='multi_csv_heatmap'
    )
    
    return app

# ====================================================================
# Example 2: Dictionary Format with Custom Display Names
# ====================================================================

def example_dict_format():
    """
    Example using a dictionary with custom display names.
    More control over how datasets appear in the dropdown.
    """
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return """
        <h1>Environmental Noise Monitoring</h1>
        <p>Select different datasets to analyze:</p>
        <ul>
            <li><a href="/noise-analysis/">Noise Analysis Dashboard</a></li>
            <li><a href="/noise-analysis/propagation">Propagation Simulation</a></li>
        </ul>
        """
    
    # Configure with custom display names
    csv_files = {
        'Airgun Survey 2023 - Primary': 'data/surveys/airgun_2023_primary.csv',
        'Airgun Survey 2023 - Secondary': 'data/surveys/airgun_2023_secondary.csv',
        'Baseline Measurements': 'data/baseline/environmental_baseline.csv',
        'Traffic Noise Study': 'data/traffic/traffic_noise_measurements.csv',
        'Construction Impact': 'data/construction/construction_noise.csv'
    }
    
    register_heatmap(app,
        CSV_FILES=csv_files,
        DEFAULT_CSV='Airgun Survey 2023 - Primary',
        URL_PREFIX='/noise-analysis',
        BLUEPRINT_NAME='environmental_noise',
        INITIAL_HEATMAP_RADIUS=50,
        INITIAL_HEATMAP_INTENSITY=1.8
    )
    
    return app

# ====================================================================
# Example 3: Dynamic CSV Configuration (Runtime Updates)
# ====================================================================

class DynamicCSVConfig:
    """
    A configuration class that can be updated at runtime.
    Useful for applications that generate CSV files dynamically.
    """
    
    def __init__(self):
        self.csv_files = {
            'Default Dataset': 'data/data.csv'
        }
        self.default_csv = 'Default Dataset'
    
    def add_csv_file(self, name, filepath):
        """Add a new CSV file to the available options"""
        self.csv_files[name] = filepath
        print(f"Added CSV file: {name} -> {filepath}")
    
    def remove_csv_file(self, name):
        """Remove a CSV file from the available options"""
        if name in self.csv_files:
            del self.csv_files[name]
            print(f"Removed CSV file: {name}")
    
    def set_default(self, name):
        """Set the default CSV file"""
        if name in self.csv_files:
            self.default_csv = name
            print(f"Set default CSV to: {name}")

def example_dynamic_config():
    """
    Example with dynamic CSV configuration that can be updated at runtime.
    """
    
    app = Flask(__name__)
    
    # Create dynamic config
    csv_config = DynamicCSVConfig()
    
    @app.route('/')
    def home():
        return """
        <h1>Dynamic CSV Configuration Example</h1>
        <p>This example shows how to dynamically add/remove CSV files.</p>
        <ul>
            <li><a href="/dynamic-heatmap/">Dynamic Heatmap</a></li>
            <li><a href="/admin/add-csv">Add New CSV (Admin)</a></li>
        </ul>
        """
    
    @app.route('/admin/add-csv')
    def admin_add_csv():
        """Simulate adding a new CSV file"""
        import time
        timestamp = int(time.time())
        csv_config.add_csv_file(
            f'Survey {timestamp}', 
            f'data/survey_{timestamp}.csv'
        )
        return f"Added new CSV file: Survey {timestamp}"
    
    # Create blueprint with dynamic config
    heatmap_config = HeatmapConfig(
        CSV_FILES=csv_config.csv_files,
        DEFAULT_CSV=csv_config.default_csv,
        URL_PREFIX='/dynamic-heatmap',
        BLUEPRINT_NAME='dynamic_heatmap'
    )
    
    blueprint = create_heatmap_blueprint(heatmap_config)
    app.register_blueprint(blueprint)
    
    return app

# ====================================================================
# Example 4: Multiple Heatmap Instances with Different Configurations
# ====================================================================

def example_multiple_instances():
    """
    Example with multiple heatmap instances for different types of data.
    """
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return """
        <h1>Multi-Instance Heatmap Dashboard</h1>
        <p>Different heatmap instances for different data types:</p>
        <ul>
            <li><a href="/airgun-data/">Airgun Survey Data</a></li>
            <li><a href="/seismic-data/">Seismic Activity Data</a></li>
            <li><a href="/environmental-data/">Environmental Monitoring</a></li>
        </ul>
        """
    
    # Airgun survey data
    airgun_csvs = {
        'Survey Zone A': 'data/airgun/zone_a.csv',
        'Survey Zone B': 'data/airgun/zone_b.csv',
        'Survey Zone C': 'data/airgun/zone_c.csv'
    }
    
    register_heatmap(app,
        CSV_FILES=airgun_csvs,
        DEFAULT_CSV='Survey Zone A',
        URL_PREFIX='/airgun-data',
        BLUEPRINT_NAME='airgun_surveys',
        COLORS_DIR='colors/airgun',
        INITIAL_HEATMAP_RADIUS=40
    )
    
    # Seismic activity data
    seismic_csvs = {
        'Last 30 Days': 'data/seismic/recent.csv',
        'Last 90 Days': 'data/seismic/quarterly.csv',
        'Annual Data': 'data/seismic/annual.csv'
    }
    
    register_heatmap(app,
        CSV_FILES=seismic_csvs,
        DEFAULT_CSV='Last 30 Days',
        URL_PREFIX='/seismic-data',
        BLUEPRINT_NAME='seismic_activity',
        COLORS_DIR='colors/seismic',
        INITIAL_HEATMAP_RADIUS=60,
        INITIAL_HEATMAP_INTENSITY=2.0
    )
    
    # Environmental monitoring data
    env_csvs = {
        'Temperature': 'data/environment/temperature.csv',
        'Humidity': 'data/environment/humidity.csv',
        'Air Quality': 'data/environment/air_quality.csv',
        'Noise Levels': 'data/environment/noise.csv'
    }
    
    register_heatmap(app,
        CSV_FILES=env_csvs,
        DEFAULT_CSV='Temperature',
        URL_PREFIX='/environmental-data',
        BLUEPRINT_NAME='environmental_monitoring',
        COLORS_DIR='colors/environmental',
        INITIAL_HEATMAP_RADIUS=35,
        DEFAULT_MAP_OPACITY=0.8
    )
    
    return app

# ====================================================================
# Example 5: Integration with Database/API
# ====================================================================

def example_database_integration():
    """
    Example showing how to integrate with a database or API
    to dynamically generate the list of available CSV files.
    """
    
    app = Flask(__name__)
    
    def get_available_datasets():
        """
        Simulate fetching available datasets from a database or API.
        In real implementation, this would query your database.
        """
        # This could be a database query, API call, etc.
        return {
            'Latest Survey': 'generated_data/latest_survey.csv',
            'Processed Results': 'generated_data/processed_results.csv',
            'Filtered Data': 'generated_data/filtered_data.csv'
        }
    
    @app.route('/')
    def home():
        return """
        <h1>Database-Driven Heatmap</h1>
        <p>CSV files are dynamically loaded from database/API.</p>
        <ul>
            <li><a href="/db-heatmap/">Database Heatmap</a></li>
            <li><a href="/refresh-datasets">Refresh Available Datasets</a></li>
        </ul>
        """
    
    @app.route('/refresh-datasets')
    def refresh_datasets():
        """Simulate refreshing the dataset list"""
        datasets = get_available_datasets()
        return f"Found {len(datasets)} datasets: {list(datasets.keys())}"
    
    # Get datasets dynamically
    available_datasets = get_available_datasets()
    
    register_heatmap(app,
        CSV_FILES=available_datasets,
        DEFAULT_CSV=list(available_datasets.keys())[0],
        URL_PREFIX='/db-heatmap',
        BLUEPRINT_NAME='database_heatmap'
    )
    
    return app

# ====================================================================
# Run Examples
# ====================================================================

if __name__ == '__main__':
    import sys
    
    examples = {
        'list': example_list_format,
        'dict': example_dict_format,
        'dynamic': example_dynamic_config,
        'multiple': example_multiple_instances,
        'database': example_database_integration
    }
    
    if len(sys.argv) > 1 and sys.argv[1] in examples:
        example_name = sys.argv[1]
        app = examples[example_name]()
        print(f"Running {example_name} example...")
        app.run(debug=True)
    else:
        print("Usage: python multi_csv_example.py [example_type]")
        print("Available examples:")
        for name, func in examples.items():
            print(f"  {name} - {func.__doc__.strip().split('.')[0]}")
        print("\nExample: python multi_csv_example.py list") 