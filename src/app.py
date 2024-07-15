from flask import Flask, request, jsonify
import uuid
import re
import math
from datetime import datetime

app = Flask(__name__)

receipts = {}

#Post method to generate id and calculate the points
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.get_json()

    if not validate_receipt(data):
        return jsonify({"error": "Invalid receipt data"}), 400

    receipt_id = str(uuid.uuid4())
    points = calculate_points(data)
    data['id'] = receipt_id
    data['points'] = points

    receipts[receipt_id] = data

    return jsonify({"id": receipt_id})

#GET method to return the points of receipt
@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    receipt = receipts.get(receipt_id)

    if receipt is None:
        return jsonify({"error": "Receipt not found"}), 404

    return jsonify({"points": receipt['points']})

#Validating the contents of receipt
def validate_receipt(receipt):
    required_keys = {"retailer", "purchaseDate", "purchaseTime", "items", "total"}
    if not required_keys.issubset(receipt):
        return False

    if not isinstance(receipt['retailer'], str) or not re.match(r"^[\w\s\-&]+$", receipt['retailer']):
        return False

    try:
        datetime.strptime(receipt['purchaseDate'], "%Y-%m-%d")
        datetime.strptime(receipt['purchaseTime'], "%H:%M")
    except ValueError:
        return False

    if not isinstance(receipt['items'], list) or len(receipt['items']) == 0:
        return False

    for item in receipt['items']:
        if 'shortDescription' not in item or 'price' not in item:
            return False
        if not isinstance(item['shortDescription'], str) or not re.match(r"^[\w\s\-]+$", item['shortDescription']):
            return False
        if not re.match(r"^\d+\.\d{2}$", item['price']):
            return False

    if not re.match(r"^\d+\.\d{2}$", receipt['total']):
        return False

    return True

#Calculates points for the receipt
def calculate_points(receipt):
    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name.
    points += len(re.findall(r'[a-zA-Z0-9]', receipt['retailer']))

    # Rule 2: 50 points if the total is a round dollar amount with no cents.
    total = float(receipt['total'])
    if total.is_integer():
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25.
    if total % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt.
    points += (len(receipt['items']) // 2) * 5

    # Rule 5: Points based on the trimmed length of the item description.
    for item in receipt['items']:
        trimmed_desc = item['shortDescription'].strip()
        if len(trimmed_desc) % 3 == 0:
            price = float(item['price'])
            points += math.ceil(price * 0.2)

    # Rule 6: 6 points if the day in the purchase date is odd.
    purchase_date = datetime.strptime(receipt['purchaseDate'], "%Y-%m-%d")
    if purchase_date.day % 2 != 0:
        points += 6

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    purchase_time = datetime.strptime(receipt['purchaseTime'], "%H:%M")
    if purchase_time.hour == 14 or (purchase_time.hour == 15 and purchase_time.minute < 60):
        points += 10

    return points

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
