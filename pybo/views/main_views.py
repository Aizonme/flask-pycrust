from flask import Blueprint, render_template, url_for
from pybo.models import Question
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, pybo!'

@bp.route('/')
def index():
    return redirect(url_for('lecture.lectures'))