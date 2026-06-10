from app.api import api
from flask import jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Post

@api.route("/users")
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@api.route("/users/<int:user_id>")
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200


@api.route("/posts")
def get_posts():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200


@api.route("/posts/<int:post_id>")
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict()), 200


@api.route("/posts", methods=["POST"])
@login_required
def create_post():
    data = request.get_json()
    content = data.get("content")
    if not content:
        return jsonify({"message": "Content is required"}), 400
    new_post = Post(content=content, user_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201


@api.route("/posts/<int:post_id>", methods=["DELETE"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        return jsonify({"message": "Unauthorized"}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"}), 200