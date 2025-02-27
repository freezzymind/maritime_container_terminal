import json

class ShipDataFormatter:
    @staticmethod
    def json_format(data):
        return json.dumps(data).encode('utf-8')