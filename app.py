from flask import Flask, request, jsonify
import os
import csv
from io import StringIO

app = Flask(__name__)

PV_DIR = "/Bindu_PV_dir "

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    
    # Validate input
    if not data or 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400
    
    if 'product' not in data:
        return jsonify({"file": data['file'], "error": "Invalid JSON input."}), 400
    
    file_path = os.path.join(PV_DIR, data['file'])
    
    # Check if file exists
    if not os.path.exists(file_path):
        return jsonify({"file": data['file'], "error": "File not found."}), 404
    
    try:
        # Read file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse CSV
        reader = csv.reader(StringIO(content))
        header = next(reader)
        
        # Find product and amount columns
        product_col = -1
        amount_col = -1
        for i, col in enumerate(header):
            if col.strip().lower() == "product":
                product_col = i
            elif col.strip().lower() == "amount":
                amount_col = i
        
        if product_col == -1 or amount_col == -1:
            return jsonify({"file": data['file'], "error": "Input file not in CSV format."}), 400
        
        # Calculate sum
        total = 0
        for row in reader:
            if len(row) > max(product_col, amount_col):
                if row[product_col].strip() == data['product']:
                    total += int(row[amount_col].strip())
        
        return jsonify({"file": data['file'], "sum": total}), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"file": data['file'], "error": "Input file not in CSV format."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)