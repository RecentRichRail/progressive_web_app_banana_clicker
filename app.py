from flask import Flask, redirect, request
import requests
import os
from dotenv import load_dotenv

from resources.banana import bp as BananaBlueprint

load_dotenv()

app = Flask(__name__, static_url_path='/internal/banana/static')

app.short_session_cookie_name = os.environ.get('short_session_cookie_name')
host_port = os.environ.get('host_port')
app.allow_logging = os.environ.get('allow_logging')
require_hanko_login = os.environ.get('require_hanko_login')
app.authentication_server = os.environ.get('authentication_server')
app.mysql_database_api = os.environ.get('mysql_database_api')

@app.before_request
def validate_jwt():
    if request.path.startswith('/external') or request.path.startswith('/static'):
        return

    print("Getting JWT")
    jwt_token = request.cookies.get(app.short_session_cookie_name)

    if not jwt_token:
        print("No JWT found")
        redirect_url = request.url
        return redirect(f"/external/login?redirect={redirect_url}")

    print("Awaiting response from server.")
    response = requests.post(f"http://{app.authentication_server}/apiv1/auth/verify_user_jwt", json={"jwt": jwt_token, "request_url": request.url, "request_ip_source": request.headers.get('X-Forwarded-For', request.remote_addr)})
    print("Server responded")
    verification_result = response.json()

    if not verification_result["valid"]:
        print("JWT not valid")
        redirect_url = request.url
        return redirect(f"/external/login?redirect={redirect_url}")

app.register_blueprint(BananaBlueprint)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=host_port, debug=True)
