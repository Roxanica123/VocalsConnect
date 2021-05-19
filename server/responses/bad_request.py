import json

from flask import Response


class BadRequest(Response):
    def __init__(self, message: str, status_code=400):
        super().__init__(status=status_code)
        self.headers['Access-Control-Allow-Origin'] = '*'
        self.data = json.dumps({"error": message})
