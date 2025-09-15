#!/usr/bin/env python3
"""
Simple Backend Server for NutriVeda Platform
"""

import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import os
import hashlib
import time

# Simple user database
USERS = {
    'admin@nutriveda.com': {
        'password': 'admin123',
        'role': 'admin',
        'name': 'Dr. Rajesh Kumar',
        'id': 1
    },
    'patient@nutriveda.com': {
        'password': 'patient123',
        'role': 'patient',
        'name': 'Priya Sharma',
        'id': 2
    }
}

# Active sessions
SESSIONS = {}

class NutriVedaHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            self.send_error(404)
    
    def handle_api_request(self):
        """Handle API requests"""
        try:
            if self.path == '/api/login/':
                self.handle_login()
            elif self.path == '/api/logout/':
                self.handle_logout()
            elif self.path == '/api/patients/':
                self.send_patients_response()
            elif self.path == '/api/diet-charts/':
                self.send_diet_charts_response()
            elif self.path == '/api/food-database/':
                self.send_food_database_response()
            else:
                self.send_json_response({'error': 'API endpoint not found'}, 404)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def send_patients_response(self):
        """Send sample patients data"""
        patients = [
            {
                "id": 1001,
                "name": "Raj Kumar",
                "age": 35,
                "gender": "Male",
                "prakriti": "Vata",
                "phone": "+91-9876543210",
                "email": "raj@email.com"
            },
            {
                "id": 1002,
                "name": "Priya Sharma", 
                "age": 28,
                "gender": "Female",
                "prakriti": "Pitta",
                "phone": "+91-9876543211",
                "email": "priya@email.com"
            },
            {
                "id": 1003,
                "name": "Amit Patel",
                "age": 42,
                "gender": "Male", 
                "prakriti": "Kapha",
                "phone": "+91-9876543212",
                "email": "amit@email.com"
            }
        ]
        self.send_json_response({"patients": patients})
    
    def send_diet_charts_response(self):
        """Send diet charts response"""
        response = {"message": "Diet chart generated successfully", "status": "success"}
        self.send_json_response(response)
    
    def send_food_database_response(self):
        """Send food database response"""
        foods = [
            {"id": 1, "name": "Rice", "category": "Grains", "calories": 130, "virya": "Cold"},
            {"id": 2, "name": "Ghee", "category": "Fats", "calories": 112, "virya": "Hot"},
            {"id": 3, "name": "Mung Dal", "category": "Legumes", "calories": 104, "virya": "Cold"}
        ]
        self.send_json_response({"foods": foods})
    
    def handle_login(self):
        """Handle login requests"""
        if self.command == 'POST':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            username = data.get('username', '')
            password = data.get('password', '')
            role = data.get('role', '')
            
            if username in USERS and USERS[username]['password'] == password and USERS[username]['role'] == role:
                # Create session
                session_id = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()
                SESSIONS[session_id] = {
                    'username': username,
                    'role': USERS[username]['role'],
                    'name': USERS[username]['name'],
                    'id': USERS[username]['id'],
                    'created': time.time()
                }
                
                self.send_json_response({
                    'success': True,
                    'session_id': session_id,
                    'user': {
                        'name': USERS[username]['name'],
                        'role': USERS[username]['role'],
                        'id': USERS[username]['id']
                    }
                })
            else:
                self.send_json_response({'success': False, 'error': 'Invalid credentials'}, 401)
        else:
            self.send_json_response({'error': 'Method not allowed'}, 405)
    
    def handle_logout(self):
        """Handle logout requests"""
        if self.command == 'POST':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            session_id = data.get('session_id', '')
            if session_id in SESSIONS:
                del SESSIONS[session_id]
                self.send_json_response({'success': True, 'message': 'Logged out successfully'})
            else:
                self.send_json_response({'success': False, 'error': 'Invalid session'}, 401)
        else:
            self.send_json_response({'error': 'Method not allowed'}, 405)
    
    def send_json_response(self, data, status=200):
        """Send JSON response with CORS headers"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

if __name__ == "__main__":
    PORT = 8000
    print("🕉️  NutriVeda Simple Backend Starting...")
    print(f"🌐 Backend running on: http://localhost:{PORT}")
    print("📊 API endpoints available:")
    print("   - /api/login/")
    print("   - /api/logout/")
    print("   - /api/patients/")
    print("   - /api/diet-charts/")
    print("   - /api/food-database/")
    print("✅ Ready to serve requests!")
    
    with socketserver.TCPServer(("", PORT), NutriVedaHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Backend server stopped")