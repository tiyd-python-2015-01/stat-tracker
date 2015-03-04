from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user

from ..extensions import db
from ..forms import LoginForm, RegistrationForm, ActivityForm, EditForm
from ..models import Activity, User, Stats

activity = Blueprint("activity", __name__)


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@activity.route("/activity", methods=["GET", "POST"])
def act():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity.query.filter_by(title=form.title.data).first()
        if activity:
            flash("An activity with that title aready exists")
        else:
            activity = Activity(title=form.title.data,
                                description=form.description.data,
                                user_id=current_user.id)
            db.session.add(activity)
            db.session.commit()
            stats = Stats(value=form.value.data,
                          recorded_at=form.recorded_at.data,
                          user_id=current_user.id,
                          act_id=activity.id)

            db.session.add(stats)
            db.session.commit()
            flash("You have successfully logged an activity")
            return render_template("activities.html", form=form)
    else:
        flash_errors(form)
    return render_template("activities.html", form=form)


@activity.route("/delete/<int:id>", methods=["GET"])
def delete_activity(id):
    stats = Stats.query.get(id)
    activity = Activity.query.get(Stats.act_id)
    db.session.delete(stats)
    db.session.commit()
    flash("The stat has been deleted.")
    return redirect(url_for("activity.act", id=activity.id))

# @activity.route('/activities/<int:id>/', methods=["DELETE"])
# def delete_activity(id):
#     if request.method == "DELETE":
#         activity = Activity.query.get(id)
#         db.session.delete(activity)
#         db.session.commit()
#     return {'Deleted': id }


@activity.route("/activity/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_activity(id):
    stats = Stats.query.get(id)
    form = EditForm(obj=stats)
    if form.validate_on_submit():
        form.populate_obj(stats)
        db.session.add(stats)
        db.session.commit()
        flash("Activity stat has been updated.")
        return redirect(url_for("activity.view_activity", id = stats.act_id))
    else:
        flash_errors(form)

    return render_template("edit.html",
                           form=form,
                           post_url=url_for("activity.edit_activity", id=stats.id),
                           button="Update Activity")

@activity.route("/activity/<int:id>", methods = ["GET", "POST"])
def view_activity(id):
    activity = Activity.query.filter_by(id = id).first()
    stats = Stats.query.filter_by(act_id = id).all()
    form = EditForm()

    if form.validate_on_submit():
        stat = Stats(user = current_user,
                     act_id = id,
                     recorded_at = form.recorded_at.data,
                     value = form.value.data)
        db.session.add(stat)
        db.session.commit()
        flash("Stat Added!")
        return redirect(url_for("activity.view_activity", id=id))

    return render_template("activity.html", form=form, stats=stats,
                           activity=activity)
