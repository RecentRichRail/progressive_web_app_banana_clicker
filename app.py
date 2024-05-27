from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HANKO_API_URL = os.environ.get('HANKO_API_URL')

app = Flask(__name__)

# Middleware to validate JWT
@app.before_request
def validate_jwt():
    # Exclude validation for certain routes
    if request.path == '/external' or request.path == '/login' or request.path.startswith('/static'):
        return

    print("Getting JWT")
    jwt_token = request.cookies.get("hanko")

    if not jwt_token:
        print("No JWT found")
        redirect_url = request.url
        return redirect(f"/login?redirect={redirect_url}")

    # Forward JWT to Script B for verification
    print("Awaiting response from server.")
    response = requests.post("http://127.0.0.1:2568/apiv1/verify_user_jwt", json={"jwt": jwt_token})
    print("Server responded")
    verification_result = response.json()

    # Handle verification result
    if not verification_result["valid"]:
        print("JWT not valid")
        redirect_url = request.url
        return redirect(f"/login?redirect={redirect_url}")

@app.route('/login')
def login():
    redirect_url = request.args.get('redirect', default='/')
    # Render login page
    return render_template('login.html', API_URL=HANKO_API_URL, redirect=redirect_url)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
