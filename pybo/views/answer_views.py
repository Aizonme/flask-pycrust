from flask import Blueprint, render_template, url_for, request, g, session, flash
from werkzeug.utils import redirect
from datetime import datetime

from pybo import db
from pybo.models import Question, Answer, Member
from pybo.forms import AnswerForm
from pybo.views.member_views import login_check

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=['POST', 'GET'])
@login_check
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    #user = Member.query.filter(Member.userId=='gamgo').first()
    if request.method == 'POST' and form.validate_on_submit():
        #content = request.form['content']
        answer = Answer(content=form.content.data, create_date=datetime.now(), question=question, member=g.user)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/modify/<int:answer_id>', methods=['POST', 'GET'])
@login_check
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.member:
        flash('수정 권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method=='POST':
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=answer.question.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', answer=answer, form=form)

@bp.route('/delete/<int:answer_id>', methods=['POST', 'GET'])
@login_check
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.member:
        flash('삭제 권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=answer.question.id))
