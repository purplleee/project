from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/77/')
def index2():
    # Logic for admin dashboard
    return "hiiiiiiiiiiiiiiii"
