from flask import Flask, jsonify, abort, request, Response
import os

app = Flask(__name__)

# ---- Configuration ----
ACCESSIBLE_IDS = set(range(1, 11))    # 1–10 → 200 OK
ROOT_DIR = os.getcwd()

SERVER_FILE_CONTENT = {               # Vulnerable files
    "robots.txt": "User-agent: *\nDisallow: /api/items/\n",
    "sitemap.xml": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset>...</urlset>",
    "ads.txt": "example.com, DIRECT, f08c47fec0942fa0\n",
    "humans.txt": "/* TEAM */\nDeveloper: Josef\n",
    "crossdomain.xml": "<?xml version=\"1.0\"?><cross-domain-policy>...</cross-domain-policy>",
    ".env": "SECRET_KEY=supersecret\nDATABASE_URL=sqlite:///app.db\n",
    ".git/config": "[core]\n\trepositoryformatversion = 0\n",
}
# ---- xxxxxxxxxxxxx ----

def serve_identifier(identifier):
    """
    Core logic for serving both IDOR and path traversal based on identifier.

    :param identifier: The identifier (ID or file path).
    """
    # IDOR: digit-only identifiers
    if identifier.isdigit():
        item_id = int(identifier)
        if item_id in ACCESSIBLE_IDS:
            return jsonify({
                "id": item_id,
                "name": f"Item {item_id}",
                "method": request.method
            }), 200
        else:
            abort(403)
    
    # Server files
    if identifier in SERVER_FILE_CONTENT:
        return Response(SERVER_FILE_CONTENT[identifier], mimetype='text/plain'), 200

    # Path traversal: treat identifier as file path
    # No sanitization: vulnerable
    target_path = os.path.join(ROOT_DIR, identifier)
    try:
        with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
        return Response(data, mimetype='text/plain'), 200
    except FileNotFoundError:
        abort(404)
    except PermissionError:
        abort(403)
    except Exception:
        abort(500)


@app.route('/api/items/<path:identifier>', methods=['GET', 'POST'])
def item_endpoint_path(identifier):
    """
    Handles GET or POST to /api/items/<identifier>.
    """
    return serve_identifier(identifier)

@app.route('/api/items', methods=['POST'])
def item_endpoint_body():
    """
    Handles POST to /api/items with JSON or form body containing 'identifier'.
    """
    # Try JSON body first
    data = request.get_json(silent=True)
    identifier = None
    if data and 'identifier' in data:
        identifier = str(data['identifier'])
    else:
        # Fallback to form-data or raw text
        identifier = request.form.get('identifier') or request.data.decode('utf-8', errors='ignore')
    if not identifier:
        # Bad request if no identifier provided
        abort(400)
    return serve_identifier(identifier)

@app.route('/<path:identifier>', methods=['GET'])
def index(identifier):
    """
    Handles GET to the root path with an identifier.
    """
    return serve_identifier(identifier)

if __name__ == '__main__':
    # Runs on http://127.0.0.1:5000 by default
    app.run(debug=True)
