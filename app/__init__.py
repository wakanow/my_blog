from flask import Flask
from config import config
from app.extensions import bootstrap, mail, moment, db, login_manager
from app.models import User, Category, Link, Post, Comment


# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    register_template_context(app)
    register_shell_context(app)


    return app

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Post=Post, Category=Category, Comment=Comment)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        user = User.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        return dict(user=user, categories=categories, links=links)

