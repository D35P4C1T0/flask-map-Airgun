# Heatmap Blueprint Examples

This folder contains example scripts demonstrating different ways to integrate and use the heatmap blueprint in your Flask applications.

## 📁 Available Examples

### 1. `simple_integration.py`
**The easiest way to get started**

```bash
python examples/simple_integration.py
```

- ✅ Minimal setup with just a few lines of code
- ✅ Single CSV file configuration
- ✅ Perfect for quick prototyping
- 🌐 Access at: `http://localhost:5000/heatmap/`

### 2. `multiple_csv_dropdown.py`
**Multiple datasets with dropdown selector**

```bash
python examples/multiple_csv_dropdown.py
```

- ✅ Multiple CSV files support
- ✅ Dropdown selector for switching datasets
- ✅ Real-time map updates
- ✅ Custom dataset names
- 🌐 Features the dropdown functionality you requested!

### 3. `advanced_configuration.py`
**Full-featured configuration example**

```bash
python examples/advanced_configuration.py
```

- ✅ Multiple heatmap instances in one app
- ✅ Custom configuration per instance
- ✅ Different URL prefixes
- ✅ Runtime configuration updates
- ✅ Advanced settings (radius, intensity, colors)
- 🌐 Multiple URLs: `/noise/` and `/environmental/`

### 4. `test_functionality.py`
**Comprehensive testing script**

```bash
python examples/test_functionality.py
```

- 🧪 Tests all endpoints and functionality
- 🧪 Verifies CSV loading and data processing
- 🧪 Checks template rendering
- 🧪 Validates API responses
- 🧪 Perfect for troubleshooting

## 🚀 Quick Start

1. **Choose an example** that matches your needs
2. **Run the script**: `python examples/[script_name].py`
3. **Open your browser** to the displayed URL
4. **Enjoy your heatmap!** 🎉

## 📋 Requirements

All examples require:
- Flask
- The heatmap blueprint files (`heatmap_blueprint.py`, etc.)
- CSV data files in the `data/` folder

## 🔧 Customization

Each example includes comments explaining:
- 📝 Configuration options
- 🎛️ Available parameters
- 🔄 How to modify for your use case
- 🎨 Styling and appearance options

## 🆘 Troubleshooting

If you encounter issues:

1. **Run the test script**: `python examples/test_functionality.py`
2. **Check the console output** for error messages
3. **Verify your CSV files** are in the correct format
4. **Ensure Flask is running** on the expected port

## 📚 Integration Patterns

### Pattern 1: Simple Single CSV
```python
from heatmap_blueprint import register_heatmap
register_heatmap(app, csv_file='data/data.csv')
```

### Pattern 2: Multiple CSV with Dropdown
```python
register_heatmap(app, csv_files={
    'Dataset 1': 'data/file1.csv',
    'Dataset 2': 'data/file2.csv'
})
```

### Pattern 3: Advanced Configuration
```python
blueprint = create_heatmap_blueprint(config={
    'CSV_FILES': {...},
    'HEATMAP_RADIUS': 25,
    'HEATMAP_INTENSITY': 2.0
})
app.register_blueprint(blueprint, url_prefix='/custom')
```

## 🎯 Next Steps

After trying these examples:
1. Adapt the configuration to your specific data
2. Customize the appearance and behavior
3. Integrate into your existing Flask application
4. Add additional features as needed

Happy mapping! 🗺️✨ 