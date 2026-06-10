from app.users import users
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app import db
from app.models import User, Post

@users.route("/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).all()
    return render_template("users/profile.html", user=user, posts=posts)

@users.route("/follow/<username>", methods=["POST"])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user == user:
        flash("You cannot follow yourself!", "danger")
        return redirect(url_for("users.profile", username=username))
    if user in current_user.following:
        flash(f"You are already following {username}!", "info")
        return redirect(url_for("users.profile", username=username))
    current_user.following.append(user)
    db.session.commit()
    flash(f"You are now following {username}!", "success")
    return redirect(url_for("users.profile", username=username))

@users.route("/unfollow/<username>", methods=["POST"])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user not in current_user.following:
        flash(f"You are not following {username}!", "info")
        return redirect(url_for("users.profile", username=username))
    current_user.following.remove(user)
    db.session.commit()
    flash(f"You have unfollowed {username}!", "success")
    return redirect(url_for("users.profile", username=username))
    

@users.route("/search")
@login_required
def search():
    q=request.args.get("q", "")

    if q:
        results=User.query.filter(User.username.contains(q)).all()

    else:
        results=[]

    return render_template("users/search.html", results=results, query=q)