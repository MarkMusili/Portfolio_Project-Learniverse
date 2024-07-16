#!/usr/bin/python3

from flask import request, abort

def get_request_data(fields):
    """
    Utility function to get and validate JSON data from the request.
    """
    data = {}
    for field in fields:
        value = request.json.get(field)
        if not value:
            abort(400, description=f"Missing {field}")
        data[field] = value
    return data
