"""This package helps with serialize mongo objects in flask."""
import datetime
from flask import json
from bson.objectid import ObjectId


class MongoJsonEncoder(json.JSONEncoder):
    """."""

    def default(self, obj):
        """."""
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class Serializer:
    """."""

    def __init__(self, app):
        """."""
        self.app = app

    def jsonify(self, *args, **kwargs):
        """Function jsonify with support for MongoDB ObjectId."""
        indent = None
        separators = (',', ':')

        if self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] or self.app.debug:
            indent = 2
            separators = (', ', ': ')

        if args and kwargs:
            raise TypeError(
                'jsonify() behavior undefined when passed both args and kwargs'
            )
        elif len(args) == 1:  # single args are passed directly to dumps()
            data = args[0]
        else:
            data = args or kwargs

        return self.app.response_class(
            (json.dumps(
                data, indent=indent,
                separators=separators, cls=MongoJsonEncoder),
             '\n'),
            mimetype=self.app.config['JSONIFY_MIMETYPE']
        )
