import json
from dataclasses import dataclass
from typing import List, Literal, Optional

from . import utils


@dataclass
class Path:
    example_id: str


@dataclass
class Object:
    name: str
    value: int


@dataclass
class Input:
    string_input: str
    int_input: int
    boolean_input: bool
    list_input: List[str]
    object_input: Object
    literal_input: Literal["a", "b", "c"]
    optional_input: Optional[str]


@dataclass
class Output:
    id: str
    message: str


def lambda_handler(event: Input, context) -> Output:

    example_id = event["pathParameters"].get("example_id")
    message = utils.hello_world()

    return {
        "statusCode": 200,
        "body": json.dumps({"id": example_id, "message": message}),
    }
