"""Authentication module.
"""

import os

import quart
import quart_cors
import quart_jwt_extended as jwt

api_password = os.getenv("API_PASSWORD")
if not api_password:
    raise RuntimeError("API_PASSWORD env not set")

app = quart.Blueprint("auth", __name__)
app = quart_cors.cors(app)


@app.route("/login", methods=["POST"])
async def login():
    """Gets a JWT token."""
    if not quart.request.is_json:
        return {"error": "missing JSON in request"}, 400

    request = await quart.request.json

    password = request.get("password", None)
    if not password:
        return {"error": "missing password parameter"}, 400

    if password != api_password:
        return {"error": "bad password"}, 401

    access_token = jwt.create_access_token(identity="admin")
    return {"token": access_token}, 200


@app.route("/refresh", methods=["POST"])
@jwt.jwt_required
async def refresh():
    """Refreshes a JWT token."""
    access_token = jwt.create_access_token(identity=jwt.get_jwt_identity())
    return {"token": access_token}, 200
