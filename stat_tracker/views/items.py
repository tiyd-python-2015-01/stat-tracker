from flask import render_template, flash, redirect, request, Blueprint
from flask import url_for, request, send_file
from flask.ext.login import login_required, current_user

from ..forms import LoginForm, RegistrationForm, AddBookmark
from ..models import Bookmark, User, BookmarkUser, Click
from ..extensions import db
import matplotlib.pyplot as plt
from datetime import datetime
from sqlalchemy import desc, and_
from io import BytesIO


bookmarks = Blueprint('bookmarks', __name__)

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form,
                  field).label.text, error), category)

@bookmarks.route('/dashboard/add_bookmark', methods=['POST'])
@login_required
def add_bookmark():
    form = AddBookmark()
    if form.validate_on_submit():
        url_list = BookmarkUser.query.filter_by(user_id=current_user.id).all()
        url = [item for item in url_list if item.bookmark.url==form.url.data]

        if url:
            flash("You've already shortened that URL!")
        else:
            bookmark = Bookmark(title=form.title.data,
                                url=form.url.data,
                                description=form.description.data)
            db.session.add(bookmark)
            db.session.commit()
            user_bookmark = BookmarkUser(user_id=current_user.id,
                                          item_id=bookmark.id)
            db.session.add(user_bookmark)
            db.session.commit()
            flash("You successfully added a link")
            return redirect(url_for('users.dashboard'))
    else:
        flash_errors(form)
    return redirect(url_for('users.dashboard'))

@bookmarks.route('/b/<short_url>')
def url_redirect(short_url):
    print(short_url)
    correct_url = Bookmark.query.filter_by(short_url=short_url).first()
    if correct_url:
        bookmark_user = BookmarkUser.query.filter_by(item_id=correct_url.id).first()
        add_click(correct_url.id)
        return redirect(correct_url.url)
    else:
        return redirect(url_for('users.index'))

@bookmarks.route('/dashboard/r/<int:int_id>', methods=["GET"])
@login_required
def delete_bookmark(int_id):
    deleted_object = BookmarkUser.query.filter_by(id=int_id).first()
    db.session.delete(deleted_object)
    db.session.commit()
    flash("You successfully removed that link")
    return redirect(url_for('users.dashboard'))

@bookmarks.route('/dashboard/e/<int:int_id>', methods=['POST', 'GET'])
@login_required
def edit_bookmark(int_id):
    form = AddBookmark()
    edited_object = BookmarkUser.query.filter_by(id=int_id).first()

    if form.validate_on_submit():
        edited_object.bookmark.title = form.title.data
        edited_object.bookmark.url = form.url.data
        edited_object.bookmark.short_url = shorten_url(form.url.data)
        edited_object.bookmark.description = form.description.data
        db.session.commit()
        flash("You successfully updated your bookmark")
        return redirect(url_for('users.dashboard'))
    else:
        flash_errors(form)
        return render_template("edit.html",
                               form=form,
                               edited_object=edited_object)

@bookmarks.route('/dashboard/click_stats', methods=['GET'])
@login_required
def click_stats():
    bookmarks = BookmarkUser.query.filter_by(user_id=current_user.id).all()
    return render_template("click_table.html", bookmarks=bookmarks)

@bookmarks.route('/dashboard/c/<int:int_id>', methods=['POST', 'GET'])
@login_required
def chart(int_id):
    bookmarkuser = BookmarkUser.query.get_or_404(int_id)
    return render_template("chart.html", bookmarkuser=bookmarkuser)

@bookmarks.route('/fig/<int:int_id>')
@login_required
def fig(int_id):
    bookmarkuser = BookmarkUser.query.get_or_404(int_id)
    click_data = bookmarkuser.clicks_by_day()
    dates = [c[0] for c in click_data]
    num_clicks = [c[1] for c in click_data]
    return create_chart(dates, num_clicks)


def add_click(bookmark_id):
    print(request.headers.get('User-Agent'))
    if current_user.is_active():
        user = current_user.id
    else:
        user = 0

    click = Click(item_id=bookmark_id,
                  user_id=user,
                  timestamp=datetime.now(),
                  user_ip_address=request.remote_addr,
                  user_agent=request.headers.get('User-Agent'))
    db.session.add(click)
    db.session.commit()

def create_chart(dates, num_clicks):
    fig = BytesIO()
    plt.plot_date(x=dates, y=num_clicks, fmt="-", c='#007095')
    # plt.figure(figsize=(9,5))
    plt.xticks(rotation=40, fontsize=8, color='#007095')
    plt.title('Click Count Per Day', color='#007095')
    plt.grid(True)
    plt.yticks(fontsize=8, color='#007095')
    plt.savefig(fig)
    plt.clf()
    fig.seek(0)
    return send_file(fig, mimetype="image/png")
