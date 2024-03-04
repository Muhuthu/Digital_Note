from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
database_name = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "muhuthu ian"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_name}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# check if there is a database so as not to overwrite/override it
def create_database(app):
    if not path.exists("website/" + database_name):
        db.create_all(app=app)
        print("Created Database!")
