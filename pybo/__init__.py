from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

#sqlalchemy의 sqlite 데이터베이스에서 모델을 수정할 수 없는 부분 고치기
from sqlalchemy import MetaData

# 마크다운 게시판 만들기 위한 모듈
from flaskext.markdown import Markdown

import config

#sqlalchemy의 MetaData부분
naming_convention ={
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck':'ck_%(table_name)s_%(column_0_name)s',
    'fk':'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk':'pk_%(table_name)s'
}

# db 객체를 create_app 함수 내에서 생성하면 블루프린트와 같은 다른 모듈에서 db객체를 import하여 사용할 수 없기 때문에
# 함수 밖에서 생성하고 함수 내에서는 초기화만 하여 사용하는 것
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

# 이 create_app()함수가 어플리케이션 팩토리 방식이다.
def create_app():
    app = Flask(__name__)

    # ??
    app.config.from_object(config)

    # ORM
    db.init_app(app)

    #edit for MetaData
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    # 우리가 작성한 DB 모델(tables)을 인식하기 위한 부분
    from . import models

    # BLUEPRINT
    from .views import main_views, question_views, answer_views, lecture_views, member_views
    app.register_blueprint(member_views.bp)
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(lecture_views.bp)

    # 필터 설정 부분
    from pybo.filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    #마크다운 적용
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    return app


    '''
    @app.route('/')
    def hello_pybo():
        return 'HELLO PYBO!'
    views의 main_views, blueprint 로 옮겨감
    '''
