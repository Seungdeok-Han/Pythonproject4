from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import InstrumentPost
from app.models import InstrumentPost, Like

user_bp = Blueprint('user', __name__)

@user_bp.route('/mypage')
@login_required
def mypage():
    my_posts = current_user.posts
    liked_posts = InstrumentPost.query\
        .join(Like, InstrumentPost.id == Like.post_id)\
        .filter(Like.user_id == current_user.id)\
        .all()
    return render_template('mypage.html', my_posts=my_posts, liked_posts=liked_posts)
