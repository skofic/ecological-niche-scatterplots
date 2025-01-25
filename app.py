from flask import Flask, render_template, jsonify, request
import requests
import json
from urllib.parse import urlencode

app = Flask(__name__)

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Constants
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwcmVmZXJyZWRfdXNlcm5hbWUiOiJyb290IiwiaXNzIjoiYXJhbmdvZGIiLCJpYXQiOjE3MzcyMTA3ODAsImV4cCI6MTczNzIxNDM4MH0.EUBDDP8KcBp5-sfbEGeVc8X-612l1okKqyVsE6lM79I"

def build_url(endpoint, extra_params=None):
    """Build URL with common and specific parameters"""
    base_url = f"{config['service']['host']}/{config['service']['database']}/{endpoint}"
    
    # Start with common parameters
    params = config['query_params']['common'].copy()
    
    # Add endpoint-specific parameters
    endpoint_name = endpoint.split('/')[-1]  # Extract endpoint name from full path
    if endpoint_name in config['query_params']:
        params.update(config['query_params'][endpoint_name])
    
    # Add any extra parameters
    if extra_params:
        params.update(extra_params)
    
    return f"{base_url}?{urlencode(params)}"

@app.route('/')
def index():
    return render_template('index.html', config=config)

@app.route('/api/species-list')
def get_species_list():
    endpoint = config['service']['endpoints']['species_list']
    url = build_url(endpoint, config['query_params']['species_list'])
    
    headers = {
        'Authorization': f'bearer {AUTH_TOKEN}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching species list: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/layer1-data')
def get_layer1_data():
    endpoint = config['service']['endpoints']['grid']
    url = build_url(endpoint)
    print(f"Layer 1 URL: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        x_values = [point[0] for point in data]
        y_values = [point[1] for point in data]
        
        print(f"Fetched {len(x_values)} points for grid layer")
        
        transformed_data = {
            'x': x_values,
            'y': y_values,
            'serviceUrl': url
        }
        
        return jsonify(transformed_data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching grid data: {str(e)}")
        return jsonify({'error': str(e), 'serviceUrl': url}), 500

@app.route('/api/layer2-data', methods=['POST'])
def get_layer2_data():
    data = request.json
    if not data or 'species' not in data:
        return jsonify({'error': 'No species provided'}), 400

    endpoint = config['service']['endpoints']['species']
    url = build_url(endpoint)
    print(f"Layer 2 URL: {url}")
    
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'bearer {AUTH_TOKEN}'
    }
    
    try:
        response = requests.post(url, json=[data['species']], headers=headers)
        response.raise_for_status()
        data = response.json()
        
        x_values = [point[0] for point in data]
        y_values = [point[1] for point in data]
        
        print(f"Fetched {len(x_values)} points for species")
        
        transformed_data = {
            'x': x_values,
            'y': y_values,
            'serviceUrl': url
        }
        
        return jsonify(transformed_data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching species data: {str(e)}")
        return jsonify({'error': str(e), 'serviceUrl': url}), 500

@app.route('/api/layer3-data', methods=['POST'])
def get_layer3_data():
    data = request.json
    if not data or 'unit' not in data:
        return jsonify({'error': 'No conservation unit provided'}), 400

    endpoint = config['service']['endpoints']['units']
    url = build_url(endpoint)
    print(f"Layer 3 URL: {url}")
    
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'bearer {AUTH_TOKEN}'
    }
    
    try:
        response = requests.post(url, json=[data['unit']], headers=headers)
        response.raise_for_status()
        data = response.json()
        
        x_values = [point[0] for point in data]
        y_values = [point[1] for point in data]
        
        print(f"Fetched {len(x_values)} points for conservation unit")
        
        transformed_data = {
            'x': x_values,
            'y': y_values,
            'serviceUrl': url
        }
        
        return jsonify(transformed_data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching conservation unit data: {str(e)}")
        return jsonify({'error': str(e), 'serviceUrl': url}), 500

@app.route('/api/update-config', methods=['POST'])
def update_config():
    data = request.json
    if 'pair' in data:
        config['query_params']['common']['pair'] = data['pair']
        return jsonify({'success': True})
    return jsonify({'error': 'No pair parameter provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
