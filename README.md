# Eco Route - Drive Safe, Breathe Clean 🌱

A web application that helps users find eco-friendly routes in Mysore, Karnataka, with real-time AQI and CO2 emission monitoring.

## Features

- 🔐 User authentication (Login/Signup)
- 🗺️ Interactive map with route planning
- 🌿 Eco-friendly route suggestions
- 📊 Real-time AQI and CO2 monitoring
- 🎯 Comparison between shortest and eco-friendly routes
- 🌳 Greenery view and standard map view
- 📍 Mysore-specific location data

## Project Structure

```
eco-route/
├── frontend/
│   ├── index.html              # Welcome page
│   ├── login.html              # Login page
│   ├── signup.html             # Signup page
│   ├── dashboard.html          # Main dashboard
│   ├── css/
│   │   └── style.css           # All styles
│   └── js/
│       ├── auth.js             # Authentication logic
│       └── dashboard.js        # Dashboard and map logic
├── backend/
│   ├── app.py                  # Flask backend
│   ├── requirements.txt        # Python dependencies
│   └── users.json              # User database (auto-created)
└── README.md                   # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- VS Code (recommended) or any code editor
- Modern web browser (Chrome, Firefox, Edge)

## Installation & Setup

### Step 1: Create Project Structure

1. Open VS Code
2. Create a new folder named `eco-route`
3. Open the folder in VS Code (File → Open Folder)

### Step 2: Create Frontend Files

Create the following folder structure:
```
eco-route/
├── frontend/
│   ├── css/
│   └── js/
└── backend/
```

**Create these files with the provided code:**

1. `frontend/index.html` - Welcome page
2. `frontend/login.html` - Login page
3. `frontend/signup.html` - Signup page
4. `frontend/dashboard.html` - Dashboard page
5. `frontend/css/style.css` - Stylesheet
6. `frontend/js/auth.js` - Authentication logic
7. `frontend/js/dashboard.js` - Dashboard logic

### Step 3: Create Backend Files

1. `backend/app.py` - Flask backend server
2. `backend/requirements.txt` - Python dependencies

### Step 4: Install Python Dependencies

1. Open terminal in VS Code (Terminal → New Terminal)
2. Navigate to backend folder:
   ```bash
   cd backend
   ```

3. Create a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 5: Run the Application

#### Terminal 1 - Backend Server:
```bash
cd backend
python app.py
```

The backend will start on `http://localhost:5000`

#### Terminal 2 - Frontend Server:
```bash
cd frontend
# Windows
python -m http.server 8000

# macOS/Linux
python3 -m http.server 8000
```

The frontend will be available at `http://localhost:8000`

### Step 6: Access the Application

1. Open your browser
2. Go to `http://localhost:8000`
3. You'll see the welcome page
4. Click "Sign Up" to create an account
5. After signup, you'll be redirected to the dashboard

## Using the Application

### 1. Welcome Page
- View features
- Navigate to Login or Signup

### 2. Signup/Login
- Create an account or login
- Credentials are stored securely with hashed passwords

### 3. Dashboard
- **Plan Route**: Enter "From" and "To" locations
  - Example locations in Mysore:
    - KRS Road
    - Chamundi Hill
    - Mysore Palace
    - Bannimantap
    - Vijayanagar
    - Hebbal
    - Gokulam

- **View Routes**:
  - Red route: Shortest but high pollution
  - Green route: Eco-friendly with clean air

- **Map Controls**:
  - Standard Map: Regular street view
  - Greenery View: Satellite view showing vegetation

- **Real-time Stats**:
  - Average AQI (Air Quality Index)
  - CO2 Emissions (g/km)
  - Eco Score (0-100)
  - Route Distance

### 4. Understanding the Data

**AQI Levels:**
- 0-50: Good (Green)
- 51-100: Moderate (Yellow)
- 101+: Unhealthy (Red)

**Eco Score:**
- 80-100: Excellent
- 60-79: Good
- 40-59: Moderate
- 0-39: Poor

## API Endpoints

### Authentication

**POST** `/api/signup`
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**POST** `/api/login`
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

### Route Planning

**POST** `/api/route` (Requires Authorization header)
```json
{
  "from": "KRS Road",
  "to": "Chamundi Hill"
}
```

**GET** `/api/areas`
Returns all Mysore areas with AQI and CO2 data

## API Access Without API Key

The application uses JWT (JSON Web Token) authentication. Here's how it works:

1. **Signup/Login**: User receives a token
2. **Token Storage**: Token stored in browser localStorage
3. **API Requests**: Token sent in Authorization header
4. **No API Keys**: All requests use the same backend URL

## Configuration

### Backend Configuration (app.py)

```python
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
```

**Important**: Change the secret key in production!

### Frontend Configuration (auth.js & dashboard.js)

```javascript
const API_URL = 'http://localhost:5000/api';
```

Change this URL when deploying to production.

## Troubleshooting

### Issue: CORS Error
**Solution**: Ensure Flask-CORS is installed and backend is running

### Issue: Connection Refused
**Solution**: Check that backend server is running on port 5000

### Issue: Map Not Loading
**Solution**: Check internet connection (Leaflet and tiles load from CDN)

### Issue: Routes Not Appearing
**Solution**: Enter valid Mysore location names from the list provided

### Issue: Login Fails
**Solution**: Check that users.json is created in backend folder

## VS Code Extensions (Recommended)

- Python
- HTML CSS Support
- JavaScript (ES6) code snippets
- Prettier - Code formatter

## Development Tips

### Debug Mode
Backend runs in debug mode by default. Changes to Python files auto-reload.

### Console Logging
Check browser console (F12) for frontend errors
Check terminal for backend errors

### Database
User data stored in `users.json` (auto-created)
- Simple JSON file database
- For production, use PostgreSQL or MongoDB

## Future Enhancements

- Real AQI API integration
- Google Maps integration
- Route history
- User preferences
- Mobile app
- More Karnataka cities

## Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript (ES6)
- Leaflet.js (Maps)
- OpenStreetMap

### Backend
- Python 3
- Flask (Web Framework)
- JWT (Authentication)
- Werkzeug (Security)

## Security Notes

- Passwords are hashed using Werkzeug
- JWT tokens expire after 7 days
- Always use HTTPS in production
- Change SECRET_KEY in production
- Don't commit sensitive data to Git

## Contributing

Feel free to fork and contribute to this project!

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check:
1. Terminal output for errors
2. Browser console for frontend issues
3. README troubleshooting section

---

**Happy Eco-Routing! Drive Safe, Breathe Clean! 🌱🚗**# ecopath
