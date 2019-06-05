from flask_sqlalchemy import SQLAlchemy


class MYSQL():
    def load(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://mananwadhwa4:password@localhost/project'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['SQLALCHEMY_POOL_SIZE'] = 100
        app.config['SQLALCHEMY_POOL_RECYCLE'] = 900
        return SQLAlchemy(app)

