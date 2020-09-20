from flask import Blueprint, url_for, request, render_template, flash, g
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Member, Lecture
from pybo.forms import LectureForm, AnswerForm
from datetime import datetime

from pybo.views.member_views import login_check

bp = Blueprint('lecture', __name__, url_prefix='/lecture')

@bp.route('/list')
def lectures():
    page = request.args.get('page', type=int, default=1)
    lecture_list = Lecture.query.order_by(Lecture.id.desc()).paginate(page, per_page=10)
    return render_template('lecture/lecture_list.html', lecture_list=lecture_list)

@bp.route('/detail/<int:lecture_id>/')
def detail(lecture_id):
    lecture = Lecture.query.get_or_404(lecture_id)
    return render_template('lecture/lecture_detail.html', lecture=lecture)

@bp.route('/create', methods=['POST', 'GET'])
@login_check
def create():
    form = LectureForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = Member.query.filter(Member.userId=='gamgo').first()
        lecture = Lecture(member=user, subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(lecture)
        db.session.commit()
        return redirect(url_for('lecture.lectures'))
    return render_template('lecture/lecture_form.html', form=form)

@bp.route('/modify/<int:lecture_id>/', methods=['POST','GET'])
@login_check
def modify(lecture_id):
    lecture = Lecture.query.get_or_404(lecture_id)
    if g.user != lecture.member:
        flash('수정 권한이 없습니다')
        return redirect('lecture.detail', lecture_id=lecture_id)
    if request.method=='POST':
        form = LectureForm()
        if form.validate_on_submit():
            form.populate_obj(lecture)
            lecture.modify_date = datetime.now()
            db.session.commit()
            #return redirect(url_for('lecture.detail', lecture_id=lecture_id))
            return render_template('lecture/lecture_detail.html', lecture=lecture)
    else:
        form = LectureForm(obj=lecture)
    return render_template('lecture/lecture_form.html', form=form)

@bp.route('/delete/<int:lecture_id>/', methods=['POST', 'GET'])
@login_check
def delete(lecture_id):
    lecture = Lecture.query.get_or_404(lecture_id)
    if g.user != lecture.member:
        flash('삭제 권한이 없습니다')
        return redirect(url_for('lecture.detail', lecture_id=lecture_id))
    db.session.delete(lecture)
    db.session.commit()
    return redirect(url_for('lecture.lectures'))            