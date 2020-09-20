from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from flask import flash
from werkzeug.security import generate_password_hash

from pybo import db
from pybo.forms import MemberCreateForm, MemberLoginForm
from pybo.models import Member

'''로그인 처리하면서 추가하는 새로 필요한 모듈'''
from flask import session
from werkzeug.security import check_password_hash
from flask import g
''''''
'''로그인 유무 판단하는 데코레이터 생성할 때 필요한 모듈'''
import functools


bp = Blueprint('member', __name__, url_prefix='/member')

def login_check(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('member.login'))
        return view(**kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('userId')
    if user_id is None:
        g.user = None
    else:
        g.user = Member.query.filter(Member.userId==user_id).first()

@bp.route('/signin', methods=['POST', 'GET'])
def _signin():
    form = MemberCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        #member = Member.query.filter(Member.userId)
        member = Member.query.filter_by(userId=form.userId.data).first()
        if not member:
            member = Member(userId=form.userId.data, userPwd=generate_password_hash(form.userPwd.data), userEmail=form.userEmail.data)
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다')
    return render_template('member/signin.html', form=form)

@bp.route('/login', methods=['POST', 'GET'])
def login():
    form = MemberLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error=None
        user = Member.query.filter(form.userId.data==Member.userId).first()
        if not user:
            error = '존재하지 않는 아이디입니다'
        elif not check_password_hash(user.userPwd, form.userPwd.data):
            error = '올바르지 않은 비밀번호입니다'
        if error is None:
            session.clear()
            session['userId'] = user.userId
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('member/login.html', form=form)

@bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('main.index'))
