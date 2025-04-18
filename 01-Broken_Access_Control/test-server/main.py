from flask import Flask, jsonify, abort, request

app = Flask(__name__)

# ---- Configuration ----
ACCESSIBLE_IDS = set(range(1, 11))    # 1–10 → 200 OK
FORBIDDEN_IDS  = set(range(11, 21))   # 11–20 → 403 Forbidden
# ---- xxxxxxxxxxxxx ----

@app.route('/api/items/<int:item_id>', methods=['GET'])
def item_endpoint(item_id):
    # Example behavior based on ID
    if item_id in ACCESSIBLE_IDS:
        return jsonify({
            "id": item_id,
            "name": f"Item {item_id}",
            "method": request.method
        }), 200

    if item_id not in ACCESSIBLE_IDS:
        abort(403)

    abort(404)

if __name__ == '__main__':
    # Runs on http://127.0.0.1:5000 by default
    app.run(debug=True)
