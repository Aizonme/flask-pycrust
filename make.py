from pybo import db
from pybo.models import Member, Question, Answer
from datetime import datetime
from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import pybo
# Q 생성
member = Member.query.filter(Member.userId.ilike('유저아이디').all()
q = Question(subject='제목', content='내용', member=member, create_date=datetime.now())

# Q 조회
# 전체 조회
all = Question.query.all()
# 조건 조회
filtered = Question.query.filter(Question.subject.ilike('%플라스크%')).all()
'''
like, 일치하는 문자열 있는지 filter, ilike, 대소문자 구분하지 않고 문자열 일치 filter
%플라스크,  플라스크로 끝나는 문자열, 플라스크%, 플라스크로 시작하는 문자열, %플라스크%, 플라스크가 포함된 문자열이 있는지 filter
'''
print(all)
print(filtered)
# Q 수정
'''
수정하고자 하는 Question객체를 가지고 온다. filter를 이용하여
filtered.subject = '새 제목'
filtered.content = '새 내용'
db.session.commit() 
커밋 해주어야 수정된다
'''

# Q 삭제
'''
삭제하고자 하는 게시글 filter이용하여 객체로 가져오기
db.session.delete(filtered)
db.session.commit()
삭제하고 커밋해주면 된다
'''

# A 생성
member = Member.query.filter(Member.userId.ilike('유저아이디')).all()
question = Question.query.get('질문번호')
a = Answer(question=question, content='내용', member=member, create_date=datetime.now())

