from flask import Blueprint, render_template

bp = Blueprint('banana_clicker', __name__, url_prefix='/internal/banana')

@bp.route('/')
def index():
    return render_template('index.html')