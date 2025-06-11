from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import InstrumentPost
from app.models import InstrumentPost, Like

user_bp = Blueprint('user', __name__)
