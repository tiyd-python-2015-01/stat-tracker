from flask import Blueprint, flash, render_template


stats = Blueprint("stats", __name__)


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                    .format(getattr(form, field).label.text, error), category)


@stats.route("/")
def index():
    return render_template('index.html')

