from flask import Blueprint, render_template, request, url_for, g, session, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer, Member
from ..forms import QuestionForm, AnswerForm
from datetime import datetime

# login_check 어노테이션 불러오기
from pybo.views.member_views import login_check

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list')
def _list():
    page = request.args.get('page', type=int, default=1)
    question_list = Question.query.order_by(Question.id.desc()).paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create', methods=['POST', 'GET'])
@login_check
def create():
    form = QuestionForm()
    if request.method == 'POST'  and form.validate_on_submit():
        #print(form.validate_on_submit())
        #data = request.form
        #print(data.get('content'))
        #print(data.get('subject'))
        #member = Member.query.filter(Member.userId=='gamgo').first()
        question = Question(member=g.user, subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=['POST', 'GET'])
@login_check
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.member:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method=='POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question) #form에서 전달받은 내용을 기존의 객체에 다시 넣어주는 것(수정한 내용 적용임)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>', methods=['POST', 'GET'])
@login_check
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.member:
        flash('삭제 권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))
            