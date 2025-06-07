from http.server import BaseHTTPRequestHandler
from api.index import app

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        try:
            # Get the Flask response
            with app.test_client() as test_client:
                response = test_client.get(self.path)
            
            # Set status code
            self.send_response(response.status_code)
            
            # Set headers
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()
            
            # Send response body
            self.wfile.write(response.data)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(str({"error": str(e)}).encode()) 