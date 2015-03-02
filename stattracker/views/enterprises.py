from flask import Blueprint, render_template, flash, redirect, request, url_for, send_file
from flask.ext.login import login_user, logout_user, current_user, login_required

from ..extensions import db
from ..forms import LoginForm, RegistrationForm, EnterpriseForm, StatForm
from ..models import User, Enterprise, Stat

from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt

enterprises = Blueprint("enterprises", __name__)

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)

@enterprises.route("/create_enterprise", methods=["GET", "POST"])
@login_required
def create_enterprise():
    form = EnterpriseForm()
    if form.validate_on_submit():
        enterprise = Enterprise(ent_name=form.ent_name.data,
                    ent_unit=form.ent_unit.data,
                    user_id=current_user.id)
        db.session.add(enterprise)
        db.session.commit()
        return redirect(url_for("users.index"))
    flash_errors(form)
    return render_template("create_enterprise.html", form=form)

@enterprises.route("/add/<int:id>", methods = ["GET", "POST"])
@login_required
def add_stats(id):
    enterprise = Enterprise.query.get(id)
    form = StatForm()
    if form.validate_on_submit():
        stat = Stat(value=form.value.data,
                    recorded_at=form.recorded_at.data,
                    enterprise_id=enterprise.id)
        db.session.add(stat)
        db.session.commit()
        return redirect(url_for("enterprises.view_stats", ent_id=enterprise.id))
    flash_errors(form)
    return render_template("add_stats.html",
                           form=form,
                           enterprise=enterprise,
                           post_url= url_for('enterprises.add_stats', id=enterprise.id))

@enterprises.route("/view/<int:ent_id>", methods = ["GET"])
@login_required
def view_stats(ent_id):
    enterprise = Enterprise.query.get(ent_id)
    stat_list = Stat.query.filter_by(enterprise_id = ent_id).order_by(Stat.recorded_at).all()
    return render_template("enterprise_stats.html", enterprise=enterprise, stat_list=reversed(stat_list))

@enterprises.route("/editpage/<int:id>", methods=["GET", "POST"])
@login_required
def edit_page(id):
    enterprise = Enterprise.query.get(id)
    stat_list = Stat.query.filter_by(enterprise_id = id).order_by(Stat.recorded_at).all()
    return render_template("edit_stats.html", enterprise=enterprise, stat_list=reversed(stat_list))

@enterprises.route("/editstat/<int:id>", methods=["GET", "POST"])
@login_required
def edit_stats(id):
    stat = Stat.query.get(id)
    enterprise = Enterprise.query.get(stat.enterprise_id)
    stat_list = Stat.query.filter_by(enterprise_id = ent_id).order_by(Stat.recorded_at).all()
    form = StatForm(obj=stat)
    if form.validate_on_submit():
        form.populate_obj(stat)
        db.session.add(stat)
        db.session.commit()
        flash("The stat has been updated.")
        return redirect(url_for("enterprises.edit_page", id=enterprise.id))

    return render_template("add_stats.html",
                           form=form,
                           enterprise=enterprise,
                           post_url= url_for('enterprises.edit_stats', id=stat.id))

@enterprises.route("/delete/<int:id>", methods = ["GET", "POST"])
def delete_stats(id):
    stat = Stat.query.get(id)
    enterprise = Enterprise.query.get(stat.enterprise_id)
    db.session.delete(stat)
    db.session.commit()
    flash("The stat has been deleted.")
    return redirect(url_for("enterprises.edit_page", id=enterprise.id))

@enterprises.route("/enterprises/<int:id>_clicks.png")
def enterprise_chart(id):
    enterprise = Enterprise.query.get(id)
    dates = [stat.recorded_at for stat in enterprise.stats]
    values = [stat.value for stat in enterprise.stats]

    fig = BytesIO()
    # plt.plot_date(x=dates, y=values, fmt="-")
    plt.bar(dates, values)
    plt.ylabel(enterprise.ent_unit)
    plt.savefig(fig)
    plt.clf()
    fig.seek(0)
    return send_file(fig, mimetype="image/png")
