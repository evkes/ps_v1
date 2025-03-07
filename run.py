from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
from werkzeug.exceptions import HTTPException
import traceback
    
# Create the Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main dashboard"""
    try:
        # Log the request
        print(f"Index page requested from {request.remote_addr}")
        return render_template('index.html')
    except Exception as e:
        print(f"Error serving index page: {str(e)}")
        print(traceback.format_exc())
        return render_template('error.html', error=str(e)), 500

@app.route('/data')
def get_data():
    """API endpoint to get company data"""
    try:
        company_id = request.args.get('company_id', '1')
        print(f"Data requested for company {company_id}")
        company_id = str(company_id)
        
        file_path = os.path.join(r"C:\Users\Evan.PEAKSPAN-PW083Y\Desktop\ps_v1\json", f"{company_id}.json")
        
        if os.path.exists(file_path):
            print(f"Loading data from {file_path}")
            with open(file_path, "r") as file:
                data = json.load(file)
                return jsonify(data)
        else:
            print(f"File not found: {file_path}")
            return jsonify({"error": f"Company data for company id {company_id} not found"}), 404
        
    except Exception as e:
        print(f"Error in get_data: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    print(f"404 error: {request.path}")
    return render_template('error.html', error="The requested page was not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    print(f"500 error: {str(e)}")
    return render_template('error.html', error="Internal server error"), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all other exceptions"""
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    
    # Log the exception
    print(f"Unhandled exception: {str(e)}")
    print(traceback.format_exc())
    
    # Return a generic error response
    return render_template('error.html', error="An unexpected error occurred"), 500

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(debug=True, host='0.0.0.0', port=5000)