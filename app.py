from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)

PV_DIR = "/Bindu_PV_dir"

def is_valid_csv(file_path):
    """Validate CSV structure: must have 'product' and 'amount' columns."""
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames

            if "product" not in headers or "amount" not in headers or not headers:
                raise ValueError("Input file not in CSV format.")

            # Reset file pointer to read rows correctly
            csvfile.seek(0)
            next(reader)  # Skip the header row

            data = []
            for row in reader:
                try:
                    product = row["product"].strip().lower()
                    amount = float(row["amount"].strip()) if row["amount"].strip() else 0
                except ValueError:
                    amount = 0

                data.append({"product": product, "amount": amount})

            print(f"CSV Data Extracted: {data}") 
            return data
    except Exception:
        raise ValueError("Input file not in CSV format.")

@app.route('/process', methods=['POST'])
def calculate():
    try:
        data = request.json

        if data is None:
            return jsonify({"file": None, "error": "Missing JSON body.", "sum": 0}), 400
        
        if  "file" not in data or "product" not in data or not isinstance(data, dict):
            return jsonify({"file": None, "error": "Invalid JSON input.", "sum": 0}), 400

        file_name = data["file"]
        product = data["product"].strip().lower()  
        file_path = os.path.join(PV_DIR, file_name)

        if not os.path.isfile(file_path):
            print(f" File Not Found: {file_path}")
            return jsonify({"file": file_name, "error": "File not found.", "sum": 0}), 404

        try:
            csv_data = is_valid_csv(file_path)
        except ValueError as e:
            print(f" CSV Read Error: {e}")
            return jsonify({"file": file_name, "error": str(e), "sum": 0}), 400
        
        print(f"Extracted CSV Data: {csv_data}")
        
        total = sum(row["amount"] for row in csv_data if row["product"] == product)
        return jsonify({"file": file_name, "sum": int(total)}), 200

    except Exception as e:
        return jsonify({"file": None, "error": str(e), "sum": 0}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)