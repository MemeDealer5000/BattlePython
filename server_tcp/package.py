import json


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    return obj.__dict__


def unpack(data):
    return json.loads(data)


def pack(data):
    data = json.dumps(data, default=serialize)
    return bytes(data, 'utf-8')
