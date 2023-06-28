import json

from .main import lambda_handler
from .utils import hello_world


def test_lambda_handler():

    event = {
        "pathParameters": {
            "example_id": "123",
        },
    }

    response = lambda_handler(event, None)

    assert response["body"] == json.dumps({"id": "123", "message": "Hello World!"})


def test_hello_world():

    message = hello_world()

    assert message == "Hello World!"
