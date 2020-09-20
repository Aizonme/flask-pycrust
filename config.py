'''SQLAlchemy setting'''
# DB 생성과 관련된 디렉토리, 설정 관리
import os

BASE_DIR = os.path.dirname(__file__)
#print(__file__)
#/home/gamgo/projects/myproject/config.py

SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "pybo.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False


''' FLask-WTF setting '''
SECRET_KEY='SUPERSECRET'