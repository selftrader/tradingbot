# controllers/zerodha_controller.py
from flask import Blueprint, redirect, request, session, jsonify
from broker import zerodha

zerodha_bp = Blueprint('zerodha', __name__)

@zerodha_bp.route('/auth/zerodha')
def auth_zerodha():
    auth_url = zerodha.get_auth_url()
    return redirect(auth_url)

@zerodha_bp.route('/auth/zerodha/callback')
def zerodha_callback():
    auth_code = request.args.get('code')
    if not auth_code:
        return "Error: Authorization code not received.", 400

    response = zerodha.exchange_code_for_token(auth_code)
    if response.status_code == 200:
        token_data = response.json()
        session['zerodha_token'] = token_data
        return jsonify(token_data)
    else:
        return f"Error retrieving Zerodha token: {response.text}", response.status_code
