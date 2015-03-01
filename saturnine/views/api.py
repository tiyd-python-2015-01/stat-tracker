from flask import Blueprint, request

api = Blueprint("api", __name__)


@api.route("/activities", methods=["GET", "POST"])
def all_activites():
    """On GET, show a list of all activities the user is tracking with links to
    their individual pages.
    On POST, create a new activity.
    """
    pass


@api.route("/activities/<id>", methods=["GET", "PUT", "DELETE"])
def activity(id):
    """On GET, show the information about the specified activity.
    On PUT, edit the name or type of data tracked.
    On DELETE, delete the activity and its data.
    """
    pass


@api.route("/activites/<id>/stats", methods=["POST", "PUT", "DELETE"])
def alter_stat(id):
    """On POST with a JSON-specified day, add data for that day.
    On PUT with a JSON-specified day, overwrite data for an existing day.
    On DELETE with a JSON-specified day, delete data for an existing day.
    """
    pass
