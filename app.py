from flask import Flask, request, jsonify
import os
import csv
from io import StringIO

app = Flask(__name__)

PV_DIR = "/Bindu_PV_dir"

def is_valid_csv(file_path):
    """Validate CSV structure: must have 'product' and 'amount' columns."""
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            header = [col.strip().lower() for col in header]
            
            # Check required columns
            if 'product' not in header or 'amount' not in header:
                return False
            
            # Check data rows
            for row in reader:
                if len(row) != len(header):
                    return False
                
        return True
    except Exception:
        return False

@app.route('/process', methods=['POST'])
def calculate():
    data = request.json
    
    # Validate input
    if not data or 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400
    
    if 'product' not in data or not data['product']:
        return jsonify({"file": data['file'], "error": "Invalid JSON input."}), 400
    
    file_path = os.path.join(PV_DIR, data['file'])
    
    # Check if file exists
    if not os.path.exists(file_path):
        return jsonify({"file": data['file'], "error": "File not found."}), 404
    
    # Validate CSV format
    if not is_valid_csv(file_path):
        return jsonify({"file": data['file'], "error": "Input file not in CSV format."}), 400
    
    # Calculate sum
    try:
        total = 0
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['product'].strip() == data['product']:
                    total += int(row['amount'].strip())
        
        return jsonify({"file": data['file'], "sum": total}), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"file": data['file'], "error": "Input file not in CSV format."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)