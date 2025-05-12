import json

def minify_colors():
    try:
        # Read the original colors.json
        with open('colors/colors.json', 'r') as f:
            colors = json.load(f)
        
        # Write the minified version
        with open('colors/colors.min.json', 'w') as f:
            json.dump(colors, f, separators=(',', ':'))
        
        print("Successfully created colors.min.json")
    except Exception as e:
        print(f"Error during minification: {e}")

if __name__ == '__main__':
    minify_colors() 