from flask import Blueprint, render_template

super_admin_bp = Blueprint('super_admin', __name__)

@super_admin_bp.route('/44/')
def index1():
    # Logic for super admin dashboard
    return "hiiiiiiiiiiiirrrrrrrrrrr"
