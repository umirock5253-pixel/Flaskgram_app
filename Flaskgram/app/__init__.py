from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DevelopmentConfig, ProductionConfig, TestingConfig

db = SQLAlchemy()
login_manager = LoginManager()

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
# config_map maps string names to config classes
# this lets tests pass 'testing' as a string instead of importing the class

def create_app(config='development'):
# config defaults to 'development' if nothing is passed
# run.py still passes DevelopmentConfig directly — still works
# tests pass 'testing' as a string — now also works

    app = Flask(__name__)

    app.config.from_object(config_map.get(config, DevelopmentConfig))
    # config_map.get(config, DevelopmentConfig) looks up the config class by name
    # if the name isn't found it falls back to DevelopmentConfig

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.auth import auth
    from app.users import users
    from app.posts import posts
    from app.api import api

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(posts, url_prefix='/posts')
    app.register_blueprint(api, url_prefix='/api')

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/500.html'), 500

    return app