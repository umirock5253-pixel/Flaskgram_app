from app.posts import posts
from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Post

@posts.route("/feed")
@login_required
def feed():
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template("posts/feed.html", posts=all_posts)

@posts.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        content = request.form.get("content")
        new_post = Post(content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for("posts.feed"))
    return render_template("posts/create.html")

@posts.route("/delete/<int:post_id>", methods=["POST"])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for("posts.feed"))

@posts.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user in post.liked_by:
        post.liked_by.remove(current_user)
        flash("Post unliked!", "success")
    else:
        post.liked_by.append(current_user)
        flash("Post liked!", "success")
    db.session.commit()
    return redirect(url_for("posts.feed"))