from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

'''멤버 폼 만들면서 추가'''
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Length, EqualTo, Email

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 반드시 입력하셔야 합니다')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 반드시 입력하셔야 합니다')])
    
class AnswerForm(FlaskForm):
    content = TextAreaField('답변', validators=[DataRequired('내용은 반드시 입력하셔야 합니다')])

class LectureForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수사항임')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수사항임')])
    
class MemberCreateForm(FlaskForm):
    userId = StringField('아이디', validators=[DataRequired('반드시 입력하셔야 합니다'), Length(min=3,  max=25)])
    userPwd = PasswordField('비밀번호', validators=[DataRequired('반드시 입력하셔야 합니다'), EqualTo('pwdcheck', '비밀번호가 일치하지 않습니다')])
    pwdcheck = PasswordField('비밀번호 확인', validators=[DataRequired('비밀번호가 일치하지 않습니다')])
    userEmail = EmailField('이메일', validators=[DataRequired('반드시 입력하셔야 합니다'), Email()])

class MemberLoginForm(FlaskForm):
    userId = StringField('아이디', validators=[DataRequired('아이디를 입력하셔야 합니다'), Length(min=3, max=25)])
    userPwd = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 입력하셔야 합니다')])
    