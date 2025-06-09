from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import datetime
import requests
from app.models import Comment, db
from . import db
from .models import InstrumentPost, BrandInfo, GenreTag, Like, MyInstrument


YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")

main = Blueprint('main', __name__)

@main.route('/')
def index():
    selected_brand_id = request.args.get('brand', type=int)
    search_query = request.args.get('q', '').strip()
    sort = request.args.get('sort', '')
    selected_shape = request.args.get('shape', '').strip()
    selected_condition = request.args.get('condition', '').strip()

    query = InstrumentPost.query

    if selected_brand_id:
        query = query.filter_by(brand_id=selected_brand_id)
    if search_query:
        query = query.filter(
            InstrumentPost.title.ilike(f'%{search_query}%') |
            InstrumentPost.model_name.ilike(f'%{search_query}%')
        )
    if selected_shape:
        query = query.filter_by(shape=selected_shape)
    if selected_condition == '80up':
        query = query.filter(InstrumentPost.condition >= 80)
    elif selected_condition == '60up':
        query = query.filter(InstrumentPost.condition >= 60, InstrumentPost.condition < 80)
    elif selected_condition == '40up':
        query = query.filter(InstrumentPost.condition >= 40, InstrumentPost.condition < 60)
    elif selected_condition == 'under40':
        query = query.filter(InstrumentPost.condition < 40)

    if sort == 'views_desc':
        query = query.order_by(InstrumentPost.views.desc())
    elif sort == 'views_asc':
        query = query.order_by(InstrumentPost.views.asc())
    elif sort == 'price_desc':
        query = query.order_by(InstrumentPost.price.desc())
    elif sort == 'price_asc':
        query = query.order_by(InstrumentPost.price.asc())
    elif sort == 'condition_best':
        # 손상도: 최상 > 양호 > 사용감 있음 > 수리 필요 (내림차순)
        condition_order = ['최상', '양호', '사용감 있음', '수리 필요']
        query = query.order_by(db.case(
            {v: i for i, v in enumerate(condition_order)},
            value=InstrumentPost.condition
        ))
    elif sort == 'condition_worst':
        # 손상도: 수리 필요 > 사용감 있음 > 양호 > 최상 (내림차순)
        condition_order = ['수리 필요', '사용감 있음', '양호', '최상']
        query = query.order_by(db.case(
            {v: i for i, v in enumerate(condition_order)},
            value=InstrumentPost.condition
        ))
    elif sort == 'shape_asc':
        query = query.order_by(InstrumentPost.shape.asc())
    elif sort == 'shape_desc':
        query = query.order_by(InstrumentPost.shape.desc())
    else:
        query = query.order_by(InstrumentPost.created_at.desc())  # 기본 정렬

    posts = query.all()
    all_brands = BrandInfo.query.all()

    return render_template('index.html', posts=posts, all_brands=all_brands,
                           selected_brand_id=selected_brand_id,
                           search_query=search_query,
                           sort=sort,
                           selected_shape=selected_shape,
                           selected_condition=selected_condition)

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        brand_id = request.form['brand_id']
        model_name = request.form['model_name']
        shape = request.form['shape']
        condition = request.form['condition']
        price = request.form['price']
        description = request.form['description']

        # 기타(직접입력) 처리
        custom_brand = request.form.get('custom_brand')
        if brand_id == 'custom' and custom_brand:
            brand = BrandInfo.query.filter_by(name=custom_brand).first()
            if not brand:
                brand = BrandInfo(name=custom_brand)
                db.session.add(brand)
                db.session.commit()
            brand_id = brand.id
        else:
            brand_id = int(brand_id)

        images = request.files.getlist('images[]')
        image_filenames = []

        for image in images:
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.root_path, 'static/uploads', filename))
                image_filenames.append(filename)

        new_post = InstrumentPost(
            title=title,
            brand_id=int(brand_id),  # brand_id를 int로 변환
            model_name=model_name,
            shape=shape,
            condition=condition,
            description=description,
            price=price,
            user_id=current_user.id,
            images=image_filenames  # 리스트로 저장
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.index'))

    # BrandInfo DB에 있는 모든 브랜드를 알파벳순으로 가져옴 (id, name, description 모두)
    brands = BrandInfo.query.order_by(BrandInfo.name).all()
    return render_template('add.html', brands=brands)

@main.route('/api/info/<string:category>/<int:id>')
def get_info(category, id):
    if category == 'brand':
        brand = BrandInfo.query.get_or_404(id)
        return jsonify({
            'title': brand.name,
            'description': brand.description or '정보 없음'
        })
    return jsonify({'error': 'invalid category'}), 400

@main.route('/api/info/brand/<int:brand_id>')
def brand_info(brand_id):
    brand = BrandInfo.query.get_or_404(brand_id)
    return jsonify({
        "title": brand.name,
        "description": brand.description or "정보 없음"
    })


@main.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = InstrumentPost.query.get_or_404(post_id)

    # 작성자인지 확인
    if post.user_id != current_user.id:
        flash('삭제 권한이 없습니다.', 'danger')
        return redirect(url_for('main.index'))

    # 댓글도 함께 삭제
    Comment.query.filter_by(post_id=post_id).delete()
    db.session.delete(post)
    db.session.commit()
    flash('글이 삭제되었습니다.', 'success')
    return redirect(url_for('main.index'))

@main.route('/post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    post = InstrumentPost.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id, parent_id=None).order_by(Comment.created_at.asc()).all()
    for comment in comments:
        comment.replies_list = comment.replies.order_by(Comment.created_at.asc()).all()

    from_like = request.args.get("from_like")
    if not from_like:
        post.views = (post.views or 0) + 1
        db.session.commit()

    # ✅ 공통 렌더링 데이터 (YouTube 검색어가 None이 되지 않도록 보장)
    youtube_query = ""
    if post.brand and post.brand.name:
        youtube_query += post.brand.name
    if post.model_name:
        youtube_query += f" {post.model_name}"
    youtube_links = search_youtube_videos(youtube_query.strip())
    # 댓글 목록은 최신 게시글의 post_id 기준으로 한 번만 가져오도록 수정 (중복 제거)
    comments = Comment.query.filter_by(post_id=post.id, parent_id=None).order_by(Comment.created_at.asc()).all()
    for comment in comments:
        comment.replies_list = comment.replies.order_by(Comment.created_at.asc()).all()

    liked = current_user.is_authenticated and any(like.user_id == current_user.id for like in post.likes)

    # 장르 추천: 모델명+브랜드 → 브랜드만(빈 문자열) → 없으면 None
    genre_tags = None
    genre_obj = None
    if post.brand and post.model_name:
        genre_obj = GenreTag.query.filter_by(brand=post.brand.name, model_name=post.model_name).first()
    if genre_obj:
        genre_tags = genre_obj.genres.split(',')
    else:
        # 모델명 일치가 없으면 브랜드만으로 대표 장르 조회 (빈 문자열로)
        if post.brand:
            brand_genre_obj = GenreTag.query.filter_by(brand=post.brand.name, model_name="").first()
            if brand_genre_obj:
                genre_tags = brand_genre_obj.genres.split(',')
            else:
                genre_tags = None  # 브랜드도 없으면 정보 없음
        else:
            genre_tags = None

    return render_template(
        'view_post.html',
        post=post,
        youtube_links=youtube_links,
        comments=comments,
        liked=liked,
        genre_tags=genre_tags
    )


def search_youtube_videos(query, max_results=2):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{query} guitar tone review demo",
        "type": "video",
        "key": YOUTUBE_API_KEY,
        "maxResults": max_results
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        results = response.json().get("items", [])
        return [
            f"https://www.youtube.com/embed/{item['id']['videoId']}"
            for item in results if 'id' in item and 'videoId' in item['id']
        ]
    except Exception as e:
        print("YouTube API Error:", e)
        return []

from flask import jsonify

@main.route('/like/<int:post_id>', methods=['POST'])
@login_required
def toggle_like(post_id):
    post = InstrumentPost.query.get_or_404(post_id)
    existing_like = Like.query.filter_by(post_id=post.id, user_id=current_user.id).first()
    if existing_like:
        db.session.delete(existing_like)
        liked = False
    else:
        db.session.add(Like(post_id=post.id, user_id=current_user.id))
        liked = True
    db.session.commit()
    return jsonify(liked=liked, like_count=len(post.likes))

@main.route("/post/<int:post_id>/comment", methods=["POST"])
@login_required
def add_comment(post_id):
    data = request.get_json()
    content = data.get('content')
    if not content:
        return jsonify(success=False), 400
    comment = Comment(content=content, user_id=current_user.id, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify(
        success=True,
        comment_id=comment.id,
        username=current_user.username,
        timestamp=comment.created_at.strftime('%Y-%m-%d %H:%M'),
        content=comment.content,
        can_delete=(current_user.id == comment.user_id)
    )

@main.route('/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        return jsonify({'success': False}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'success': True})


@main.route('/mypage', methods=['GET', 'POST'])
@login_required
def mypage():
    if request.method == 'POST':
        brand = request.form['brand']
        model_name = request.form['model_name']
        description = request.form.get('description', '')
        images = request.files.getlist('images[]')
        image_filenames = []
        for image in images:
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.root_path, 'static/uploads', filename))
                image_filenames.append(filename)
        my_instrument = MyInstrument(
            user_id=current_user.id,
            brand=brand,
            model_name=model_name,
            images=image_filenames,
            description=description
        )
        db.session.add(my_instrument)
        db.session.commit()
        flash('내 악기가 등록되었습니다!', 'success')
        return redirect(url_for('main.mypage'))
    my_instruments = MyInstrument.query.filter_by(user_id=current_user.id).all()
    return render_template('mypage.html', my_instruments=my_instruments)

@main.route('/mypage/delete/<int:instrument_id>', methods=['POST'])
@login_required
def delete_my_instrument(instrument_id):
    instrument = MyInstrument.query.get_or_404(instrument_id)
    if instrument.user_id != current_user.id:
        flash('삭제 권한이 없습니다.', 'danger')
        return redirect(url_for('main.mypage'))
    db.session.delete(instrument)
    db.session.commit()
    flash('내 악기가 삭제되었습니다.', 'success')
    return redirect(url_for('main.mypage'))

@main.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = InstrumentPost.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('수정 권한이 없습니다.', 'danger')
        return redirect(url_for('main.view_post', post_id=post_id))
    if request.method == 'POST':
        post.title = request.form['title']
        post.brand_id = int(request.form['brand_id']) if request.form['brand_id'] != 'custom' else post.brand_id
        post.model_name = request.form['model_name']
        post.shape = request.form['shape']
        post.condition = request.form['condition']
        post.price = request.form['price']
        post.description = request.form['description']
        # 이미지 수정은 생략(필요시 추가 구현)
        db.session.commit()
        flash('게시글이 수정되었습니다.', 'success')
        return redirect(url_for('main.view_post', post_id=post.id))
    brands = BrandInfo.query.order_by(BrandInfo.name).all()
    return render_template('edit_post.html', post=post, brands=brands)