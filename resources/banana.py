from flask import Blueprint, render_template, current_app, redirect, request
import requests

bp = Blueprint('banana_clicker', __name__, url_prefix='/internal/banana')

@bp.route('/')
def index():
    response = requests.post(f"http://{current_app.mysql_database_api}/apiv1/games/banana_clicker/is_user_allowed", json={"jwt": request.cookies.get(current_app.short_session_cookie_name)})
    is_allowed = response.json()
    if is_allowed['allowed'] == False:
        print(is_allowed)
        return redirect('/internal/search')
    return render_template('index.html', user_id=is_allowed['id'])