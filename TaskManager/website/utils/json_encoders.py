"""JSON encoders"""
from datetime import datetime
import json


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder for datetime objects - default() method will return obj.isoformat() if obj is datetime instance"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)