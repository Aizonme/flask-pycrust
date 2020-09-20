from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, "pybo.db"))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY=b'\x85\xc4\xa2A\x1dR\xd3\xaa\xe1\xe5`\xae\x81\x0b\x1d&'

