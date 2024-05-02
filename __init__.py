from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from .blueprints.employee.routes import employee_bp
from .blueprints.admin.routes import admin_bp
from .blueprints.super_admin.routes import super_admin_bp
from .blueprints.common.errors import register_error_handlers
from uwu.database import db


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(employee_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(super_admin_bp, url_prefix='/super_admin')

    register_error_handlers(app)

    return app
