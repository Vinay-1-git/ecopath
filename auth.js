const API_URL = 'http://localhost:5000/api'; // Correctly set to match Flask app.run port

// Login Form Handler
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        // Clear previous errors
        clearErrors();

        try {
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                window.location.href = 'dashboard.html';
            } else {
                // Show API error message (e.g., 'Invalid email or password')
                showError('emailError', data.message || 'Login failed');
            }
        } catch (error) {
            // This catches network errors (e.g., server down, wrong port)
            showError('emailError', 'Connection error. Please try again.');
            console.error('Login error:', error);
        }
    });
}

// Signup Form Handler
if (document.getElementById('signupForm')) {
    document.getElementById('signupForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        // Clear previous errors
        clearErrors();
        
        // Validate passwords match
        if (password !== confirmPassword) {
            showError('confirmError', 'Passwords do not match');
            return;
        }
        
        // Validate password length
        if (password.length < 6) {
            showError('passwordError', 'Password must be at least 6 characters');
            return;
        }
        
        try {
            const response = await fetch(`${API_URL}/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                window.location.href = 'dashboard.html';
            } else {
                showError('emailError', data.message || 'Signup failed');
            }
        } catch (error) {
            showError('emailError', 'Connection error. Please try again.');
            console.error('Signup error:', error);
        }
    });
}

function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

function clearErrors() {
    const errors = document.querySelectorAll('.error-message');
    errors.forEach(error => {
        error.textContent = '';
        error.style.display = 'none';
    });
}

// Check if user is already logged in
function checkAuth() {
    const token = localStorage.getItem('token');
    if (token && (window.location.pathname.includes('login.html') || window.location.pathname.includes('signup.html'))) {
        window.location.href = 'dashboard.html';
    }
}

checkAuth();