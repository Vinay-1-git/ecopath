from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import json
import os
import secrets
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)
# Enable CORS for frontend running on a different port/host
CORS(app) 

# Configuration
app.config['SECRET_KEY'] = secrets.token_urlsafe(32) 
app.config['DATABASE_FILE'] = 'users.json'

# Initialize database file
if not os.path.exists(app.config['DATABASE_FILE']):
    with open(app.config['DATABASE_FILE'], 'w') as f:
        json.dump([], f)

## 🗺️ Expanded Mysore Area Data 
MYSORE_AREAS = {
    'KRS Road': {'lat': 12.3040, 'lng': 76.6397, 'aqi': 45, 'co2': 120, 'greenery': 0.8},
    'Chamundi Hill': {'lat': 12.2726, 'lng': 76.6730, 'aqi': 25, 'co2': 80, 'greenery': 0.95},
    'Mysore Palace': {'lat': 12.3051, 'lng': 76.6551, 'aqi': 85, 'co2': 180, 'greenery': 0.4},
    'Bannimantap': {'lat': 12.2857, 'lng': 76.6395, 'aqi': 65, 'co2': 150, 'greenery': 0.6},
    'Vijayanagar': {'lat': 12.3352, 'lng': 76.6291, 'aqi': 95, 'co2': 200, 'greenery': 0.3},
    'Hebbal': {'lat': 12.3269, 'lng': 76.6486, 'aqi': 75, 'co2': 160, 'greenery': 0.5},
    'Jayalakshmipuram': {'lat': 12.3196, 'lng': 76.6164, 'aqi': 55, 'co2': 130, 'greenery': 0.7},
    'Kuvempunagar': {'lat': 12.3384, 'lng': 76.6074, 'aqi': 70, 'co2': 155, 'greenery': 0.55},
    'Saraswathipuram': {'lat': 12.3260, 'lng': 76.6066, 'aqi': 60, 'co2': 140, 'greenery': 0.65},
    'Gokulam': {'lat': 12.2900, 'lng': 76.6200, 'aqi': 40, 'co2': 110, 'greenery': 0.85},
    'Airport Road': {'lat': 12.2612, 'lng': 76.6625, 'aqi': 90, 'co2': 190, 'greenery': 0.35},
    'Jayanagar': {'lat': 12.2970, 'lng': 76.6090, 'aqi': 62, 'co2': 145, 'greenery': 0.63},
    'T. Narasipura Road': {'lat': 12.2850, 'lng': 76.6800, 'aqi': 78, 'co2': 165, 'greenery': 0.5},
    'Lalitha Mahal': {'lat': 12.2885, 'lng': 76.6710, 'aqi': 30, 'co2': 90, 'greenery': 0.9},
    'Hootagalli Industrial Area': {'lat': 12.3550, 'lng': 76.5950, 'aqi': 110, 'co2': 220, 'greenery': 0.2},
    'Bogadi': {'lat': 12.2800, 'lng': 76.5900, 'aqi': 50, 'co2': 125, 'greenery': 0.75},
    'R.M. Nagar': {'lat': 12.3080, 'lng': 76.6000, 'aqi': 58, 'co2': 135, 'greenery': 0.68},
    'Zoo Road': {'lat': 12.3045, 'lng': 76.6605, 'aqi': 48, 'co2': 122, 'greenery': 0.8},
    'Yadavagiri': {'lat': 12.3175, 'lng': 76.6430, 'aqi': 80, 'co2': 170, 'greenery': 0.45},
    'Ring Road Junction (Columbia Asia)': {'lat': 12.3395, 'lng': 76.6490, 'aqi': 100, 'co2': 210, 'greenery': 0.25},
}

# Helper functions
def load_users():
    """Loads all user data from the JSON file."""
    try:
        with open(app.config['DATABASE_FILE'], 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    """Saves the current user list back to the JSON file."""
    with open(app.config['DATABASE_FILE'], 'w') as f:
        json.dump(users, f, indent=4)

def token_required(f):
    """Decorator to enforce JWT token presence and validity."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
                
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['email']
            
        except jwt.exceptions.DecodeError:
            return jsonify({'message': 'Token is invalid or expired'}), 401
        except Exception as e:
            print(f"Token error: {e}")
            return jsonify({'message': 'An error occurred during token processing'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# Haversine distance calculation
def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculates the distance (in km) between two points using the Haversine formula."""
    R = 6371  # Earth's radius in km
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def generate_shortest_route(from_data, to_data):
    """Mocks a shortest (less eco-friendly) route."""
    lat_step = (to_data['lat'] - from_data['lat']) / 3
    lng_step = (to_data['lng'] - from_data['lng']) / 3
    
    coordinates = [
        [from_data['lat'], from_data['lng']],
        [from_data['lat'] + lat_step, from_data['lng'] + lng_step],
        [from_data['lat'] + 2*lat_step, from_data['lng'] + 2*lng_step],
        [to_data['lat'], to_data['lng']]
    ]
    distance = calculate_distance(from_data['lat'], from_data['lng'], to_data['lat'], to_data['lng'])
    
    high_aqi_points = [
        {'coordinates': [from_data['lat'] + lat_step, from_data['lng'] + lng_step], 'aqi': 95, 'co2': 200},
        {'coordinates': [from_data['lat'] + 2*lat_step, from_data['lng'] + 2*lng_step], 'aqi': 105, 'co2': 210}
    ]
    
    return {
        'coordinates': coordinates,
        'distance': round(distance, 2),
        'avg_aqi': 95,
        'avg_co2': 195,
        'eco_score': 45,
        'high_aqi_points': high_aqi_points
    }

def generate_eco_route(from_data, to_data):
    """Mocks an eco-friendly (longer) route."""
    lat_diff = to_data['lat'] - from_data['lat']
    lng_diff = to_data['lng'] - from_data['lng']
    
    coordinates = [
        [from_data['lat'], from_data['lng']],
        [from_data['lat'] + lat_diff * 0.2, from_data['lng'] + lng_diff * 0.3],
        [from_data['lat'] + lat_diff * 0.4, from_data['lng'] + lng_diff * 0.5],
        [from_data['lat'] + lat_diff * 0.7, from_data['lng'] + lng_diff * 0.8],
        [to_data['lat'], to_data['lng']]
    ]
    distance = calculate_distance(from_data['lat'], from_data['lng'], to_data['lat'], to_data['lng']) * 1.15
    
    low_aqi_points = [
        {'coordinates': [from_data['lat'] + lat_diff * 0.4, from_data['lng'] + lng_diff * 0.5], 'aqi': 35, 'co2': 95},
        {'coordinates': [from_data['lat'] + lat_diff * 0.7, from_data['lng'] + lng_diff * 0.8], 'aqi': 42, 'co2': 105}
    ]
    
    return {
        'coordinates': coordinates,
        'distance': round(distance, 2),
        'avg_aqi': 48,
        'avg_co2': 115,
        'eco_score': 82,
        'low_aqi_points': low_aqi_points
    }

# Routes
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not all([name, email, password]):
        return jsonify({'message': 'All fields are required'}), 400
    
    users = load_users()
    if any(user['email'] == email for user in users):
        return jsonify({'message': 'Email already registered'}), 400
    
    new_user = {
        'name': name,
        'email': email,
        'password': generate_password_hash(password),
        'created_at': datetime.datetime.now().isoformat()
    }
    users.append(new_user)
    save_users(users)
    
    token = jwt.encode({
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({
        'message': 'Signup successful',
        'token': token,
        'user': {'name': name, 'email': email}
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'message': 'Email and password are required'}), 400
    
    users = load_users()
    user = next((u for u in users if u['email'] == email), None)
    
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    token = jwt.encode({
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {'name': user['name'], 'email': email}
    }), 200

@app.route('/api/route', methods=['POST'])
@token_required
def get_route(current_user):
    data = request.get_json()
    from_location = data.get('from', '').strip()
    to_location = data.get('to', '').strip()
    
    if not all([from_location, to_location]):
        return jsonify({'message': 'From and To locations are required'}), 400
    
    from_data = None
    to_data = None
    
    for area, area_data in MYSORE_AREAS.items():
        if area.lower() in from_location.lower():
            from_data = area_data.copy()
            from_data['name'] = area
        if area.lower() in to_location.lower():
            to_data = area_data.copy()
            to_data['name'] = area
    
    if not from_data:
        from_data = {'lat': 12.2958, 'lng': 76.6394, 'aqi': 60, 'co2': 140, 'name': from_location}
    if not to_data:
        to_data = {'lat': 12.3051, 'lng': 76.6551, 'aqi': 70, 'co2': 150, 'name': to_location}
    
    shortest_route = generate_shortest_route(from_data, to_data)
    eco_route = generate_eco_route(from_data, to_data)
    
    return jsonify({
        'shortest_route': shortest_route,
        'eco_route': eco_route,
        'message': 'Routes calculated successfully'
    }), 200

@app.route('/api/areas', methods=['GET'])
def get_areas():
    """Returns the list of all areas and their environmental data."""
    return jsonify(MYSORE_AREAS), 200

if __name__ == '__main__':
    # Ensure this is running on port 5000 to match the JS frontend
    app.run(debug=True, port=5000)