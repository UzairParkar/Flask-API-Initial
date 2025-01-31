from flask import make_response, jsonify,abort
from werkzeug.exceptions import HTTPException


class PGAPIException (HTTPException):
    def __init__(self,message, errors = None):
        payload = {'Message':message}
        if errors:
            payload ['Errors'] = errors

        abort(make_response(jsonify,(payload),400))
        
        