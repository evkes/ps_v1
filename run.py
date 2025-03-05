from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

def load_data(company_id):
    file_path = os.path.join("json", f"{company_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    company_id = request.args.get('company_id', 1)  # Default to company 1 if no ID provided
    data = load_data(company_id)
    if data:
        return jsonify(data)
    return jsonify({"error": "Company data not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
