import json

from flask import Blueprint, jsonify, request, abort, url_for
from flask.ext.login import login_user

from ..models import User, Item, Action
from ..forms import LoginForm, RegistrationForm
from ..extensions import login_manager, db


api = Blueprint("api", __name__)

def json_response(code, data):
    return (json.dumps(data), code, {"Content-Type": "application/json"})


@api.app_errorhandler(401)
def unauthorized(request):
    return ("", 401, {"Content-Type": "application/json"})


@login_manager.request_loader
def authorize_user(request):
    authorization = request.authorization
    if authorization:
        email = authorization['email']
        password = authorization['password']

        user = User.query.filter_by(email=email).first()
        if user.check_password(password):
            return user
    return None


def require_authorization():
    user = authorize_user(request)
    if user:
        login_user(user)
        return user
    else:
        abort(401)


@api.route("/bookmarks", methods=["GET", "POST"])
def bookmarks():
    if request.method == "POST":
        return create_bookmark()

    bookmarks = BookmarkUser.query.all()
    bookmarks = [bookmark.to_dict() for bookmark in bookmarks]
    return jsonify({"bookmarks": bookmarks})


def create_bookmark():
    user = require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = AddBookmark(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        url_list = BookmarkUser.query.filter_by(user_id=user.id).all()
        url = [item for item in url_list if item.bookmark.url==form.url.data]
        if url:
            return json_response(400, {"url": "This URL is taken."})
        else:
            bookmark = Bookmark(**form.data)
            db.session.add(bookmark)
            db.session.commit()
            user_bookmark = BookmarkUser(user_id=user.id,
                                          item_id=bookmark.id)
            db.session.add(user_bookmark)
            db.session.commit()
            return (json.dumps(bookmark.to_dict()), 201,
                    {"Location": url_for(".bookmark", id=bookmark.id)})
    else:
        return json_response(400, form.errors)


@api.route("/bookmarks/<int:id>")
def bookmark(id):
    bookmark = Bookmark.query.get_or_404(id)
    return jsonify(bookmark.to_dict())
