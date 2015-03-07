from functools import wraps

from flask import request, jsonify, Response, g
from flask.views import MethodView


def api_form(form_cls, *args, **kwargs):
    default_kwargs = {"formdata": None, "csrf_enabled": False}
    default_kwargs.update(kwargs)
    return form_cls(*args, **default_kwargs)

def form_to_dict(form):
    data = form.to_dict(flat=False)
    data = dict((key, value if len(value) > 1 else value[0]) for key, value in data)
    return data


def is_json():
    return request.content_type[-4:] == "json"


def accepts_json_data(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ["POST", "PUT", "PATCH"] and is_json() and not getattr(g, "data", None):
            g.data = request.get_json(silent=True)
        return f(*args, **kwargs)

    return decorated_function


def accepts_form_data(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ["POST", "PUT", "PATCH"] and not is_json() and not getattr(g, "data", None):
            g.data = form_to_dict(request.form)

        return f(*args, **kwargs)

    return decorated_function


def returns_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        retval = f(*args, **kwargs)
        if type(retval) is Response:
            return retval
        elif type(retval) is tuple:
            response = jsonify(retval[0])
            if len(retval) > 1:
                response.status_code = retval[1]
            if len(retval) > 2:
                for key, value in retval[2].items():
                    response.headers[key] = value
            return response
        else:
            return jsonify(retval)

    return decorated_function


class APIView(MethodView):
    decorators = [accepts_json_data,
                  accepts_form_data,
                  returns_json]
