from pybo import db

# sqlalchemy의 테이블과 칼럼들에 대한 설정

class Member(db.Model):
    userNum = db.Column(db.Integer, primary_key = True, autoincrement=True)
    userId = db.Column(db.String(150), unique=True, nullable = False)
    userPwd = db.Column(db.String(200), nullable = False)
    userEmail = db.Column(db.String(150), unique=True, nullable = False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    subject = db.Column(db.String(200), nullable = False)
    content = db.Column(db.Text(), nullable = False)
    userId = db.Column(db.String(200), db.ForeignKey('member.userId', ondelete='CASCADE'))
    member = db.relationship('Member', backref = db.backref('question_list'))
    create_date = db.Column(db.DateTime(), nullable = False)
    modify_date = db.Column(db.DateTime(), nullable=True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref = db.backref('answer_set'))
    content = db.Column(db.Text(), nullable = False)
    userId = db.Column(db.String(200), db.ForeignKey('member.userId', ondelete='CASCADE'))
    member = db.relationship('Member', backref = db.backref('answer_list'))
    create_date = db.Column(db.DateTime(), nullable = False)
    modify_date = db.Column(db.DateTime(), nullable=True)

class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=True)
    userId = db.Column(db.String(200), db.ForeignKey('member.userId', ondelete='CASCADE'))
    member = db.relationship('Member', backref=db.backref('lecture_list'))
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)


# db.relationship과 그 안의 backref옵션은 객체간의 상호 참조를 위한 옵션이다    
'''
A객체 B객체가 서로 상호참조하도록 해보면
class B:
    a = db.relationship('A', backref = db.backref('b_list')

b.a. 로 b객체에서 a객체를 불러올 수 있고
a.b_list로 a객체에서 해당 b객체를 불러올 수 있다
'''
