from flask import Blueprint, render_template, current_app, redirect, request
import requests

bp = Blueprint('banana_clicker', __name__, url_prefix='/internal/banana')

@bp.route('/')
def index():
    response = requests.post(f"http://{current_app.authentication_server}/apiv1/auth/get_user_info", json={"jwt": request.cookies.get(current_app.short_session_cookie_name)})
    user_info = response.json()
    if user_info['valid'] == False:
        return redirect('/internal/search')
    elif user_info['valid']:
        return render_template('index.html', user_id=user_info['sub'])