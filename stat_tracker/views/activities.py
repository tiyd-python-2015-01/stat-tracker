from datetime import datetime
from io import BytesIO

from flask import Blueprint, render_template, flash, redirect, url_for, send_file
from flask.ext.login import login_required, current_user
import matplotlib.pyplot as plt

from ..extensions import db
from ..forms import ActivityForm
from ..models import Activity, Stat


activities = Blueprint("activities", __name__)


@activities.route("/")
def index():
    activity = Activity.query.all()
    return render_template("index.html", activities=activities)


@activities.route("/activity/new", methods=["GET", "POST"])
@login_required
def new_activity():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity.query.filter_by(activity_name=form.activity_name.data).first()
        if activity:
            flash("You have already created that activity")
        else:
            activity = Activity(activity_name=form.activity_name.data,
                                measurement=form.measurement.data)
            db.session.add(activity)
            db.session.commit()
            flash("Your activity has been created.")
            return redirect(url_for("activities.index"))

    return render_template("new_activity.html",
                           form=form)
                           #post_url=url_for("books.new_book"),
                           #button="Add book)

#This would track the book clicks in the Clicks model
# @books.route("/book/<int:id>")
# def goto_book(id):
#     activity = Activity.query.get_or_404(id)
#     stat = Stat(book=book, clicked_at=datetime.now())
#     db.session.add(click)
#     db.session.commit()
#     return redirect(book.url, code=301)


@activities.route("/activity/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_activity(id):
    activity = Activity.query.get(id)
    form = ActivityForm(obj=activity)
    if form.validate_on_submit():
        form.populate_obj(activity)
        db.session.commit()
        flash("The book has been updated.")
        return redirect(url_for("activities.index"))

    return render_template("activity_form.html",
                           form=form,
                           #post_url=url_for("activity.edit_activity",
                           #id=activity.id),
                           button="Update Stat")



@activities.route("/activity/<int:id>/data")
def activities_data(id):
    activity = Activity.query.get_or_404(id)
    return render_template("activity_data.html",
                           activity=activity)


# def make_clicks_chart(book):
#     click_data = book.clicks_by_day()
#     dates = [c[0] for c in click_data]
#     date_labels = [d.strftime("%b %d") for d in dates]
#     every_other_date_label = [d if i % 2 else "" for i, d in enumerate(date_labels)]
#     num_clicks = [c[1] for c in click_data]
#
#     ax = plt.subplot(111)
#     ax.spines["top"].set_visible(False)
#     ax.spines["right"].set_visible(False)
#     ax.get_xaxis().tick_bottom()
#     ax.get_yaxis().tick_left()
#
#     plt.title("Clicks by day")
#     plt.plot_date(x=dates, y=num_clicks, fmt="-")
#     plt.xticks(dates, every_other_date_label, rotation=45, size="x-small")
#     plt.tight_layout()
#
#
# @activities.route("/book/<int:id>_clicks.png")
# def activities_clicks_chart(id):
#     book = Book.query.get_or_404(id)
#     make_clicks_chart(book)
#
#     fig = BytesIO()
#     plt.savefig(fig)
#     plt.clf()
#     fig.seek(0)
#     return send_file(fig, mimetype="image/png")
