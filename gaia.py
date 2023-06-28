import json
import os

import click

with open("cdk.json", "r") as json_file:
    context = json.load(json_file)["context"]
    cdk_name = context["name"]


@click.group()
def gaia():
    pass


@gaia.command()
@click.argument("name")
@click.option("--description", required=True, help="Description for the endpoint")
@click.option(
    "--method", required=False, help="HTTP method for the endpoint", default="POST"
)
@click.option("--belongs", help="Folder name you want to share code accross lambdas")
@click.option("--endpoint", help="Endpoint URL for the API Gateway")
@click.option("--no-api", help="Do not create an API Gateway endpoint", is_flag=True)
def create(name, description, method, belongs, endpoint, no_api):
    """
    Creates the required folder structure with the given name.
    """
    create_scaffold(name, description, method.upper(), belongs, endpoint, no_api)


def create_scaffold(
    name, description, http_method="POST", belongs=None, endpoint=None, no_api=False
):

    if endpoint and endpoint.startswith("/"):
        endpoint = endpoint[1:]

    if not belongs:
        pascal_name = "".join(word.capitalize() for word in name.split("_"))
        folder_path = os.path.join("functions", name)
        os.makedirs(folder_path, exist_ok=True)
        config = f"{pascal_name}Config"
        endpoint = endpoint or name
        comment = name
        if not no_api:
            with open(os.path.join(folder_path, "config.py"), "w") as f:
                f.write(
                    f"""from infra.services import Services


class {config}:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="{pascal_name}",
            path="./functions/{name}",
            description="{description}",
            environment={{
                "CONTROL_TABLE_NAME": services.dynamo.control_table.table_name,
            }}
        )

        services.api_gateway.create_endpoint("{http_method}", "/{endpoint}", function)

        services.dynamo.control_table.grant_read_write_data(function)
    """
                )
        else:
            with open(os.path.join(folder_path, "config.py"), "w") as f:
                f.write(
                    f"""from infra.services import Services


class {config}:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="{pascal_name}",
            path="./functions/{name}",
            description="{description}",
            environment={{
                "CONTROL_TABLE_NAME": services.dynamo.control_table.table_name,
            }}
        )

        services.dynamo.control_table.grant_read_write_data(function)
    """
                )

    else:
        folder_path = os.path.join(f"functions/{belongs}", name)
        pascal_name = "".join(word.capitalize() for word in name.split("_"))
        os.makedirs(folder_path, exist_ok=True)
        os.makedirs(f"functions/{belongs}/utils", exist_ok=True)
        open(os.path.join(f"functions/{belongs}/utils", "__init__.py"), "a").close()
        open(os.path.join(f"functions/{belongs}", "__init__.py"), "a").close()
        config = f"{pascal_name}Config"
        endpoint = endpoint or belongs
        comment = belongs
        if not no_api:
            with open(os.path.join(folder_path, "config.py"), "w") as f:
                f.write(
                    f"""from infra.services import Services


class {config}:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="{pascal_name}",
            path="./functions/{belongs}",
            directory="{name}",
            description="{description}",
            environment={{
                "CONTROL_TABLE_NAME": services.dynamo.control_table.table_name,
            }}
        )

        services.api_gateway.create_endpoint("{http_method}", "/{endpoint}", function)

        services.dynamo.control_table.grant_read_write_data(function)
    """
                )
        else:
            with open(os.path.join(folder_path, "config.py"), "w") as f:
                f.write(
                    f"""from infra.services import Services


    class {config}:
        def __init__(self, services: Services) -> None:

            function = services.aws_lambda.create_function(
                name="{pascal_name}",
                path="./functions/{belongs}",
                directory="{name}",
                description="{description}",
                environment={{
                    "CONTROL_TABLE_NAME": services.dynamo.control_table.table_name,
                }}
            )

            services.dynamo.control_table.grant_read_write_data(function)
    """
                )

    open(os.path.join(folder_path, "__init__.py"), "a").close()

    if not no_api:
        with open(os.path.join(folder_path, "integration.py"), "w") as f:
            f.write(
                f"""import pytest
    import requests
    import os

    stage = os.environ.get("STAGE", "dev")

@pytest.mark.integration(method="{http_method}", endpoint="/{endpoint}")
def test_{name}_status_code_is_200(headers, control_table):

    # Add pre-conditions here, if needed
    # control_table.put_item(Item={{ "PK": "TEST#123"}})

    response = requests.{http_method.lower()}(
        f"https://api.goentri.com/v2/{{stage}}/{cdk_name.lower()}/{endpoint}", headers=headers
    )

    # Add post-conditions here, if needed
    # control_table.delete_item(Key={{"PK": "TEST#123"}})

    assert response.status_code == 200   
    """
        )

    with open(os.path.join(folder_path, "unit.py"), "w") as f:
        f.write(
            """import json

from .main import lambda_handler


def test_lambda_handler():

    response = lambda_handler(None, None)

    assert response["body"] == json.dumps({"message": "Hello World!"})
"""
        )

    with open(f"{folder_path}/main.py", "w") as f:
        if "{" in endpoint and "}" in endpoint:
            f.write(
                """import json
from dataclasses import dataclass
import os
import boto3

# TODO: Remove this todo, uncomment the dataclasses and add the correct fields for Path, Input and Output

# @dataclass
class Path:
    pass


# @dataclass
class Input:
    pass


# @dataclass
class Output:
    pass


def lambda_handler(event: Input, context) -> Output:
    dynamodb = boto3.resource("dynamodb")
    CONTROL_TABLE_NAME = os.environ.get("CONTROL_TABLE_NAME")
    control_table = dynamodb.Table(CONTROL_TABLE_NAME)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello World!"}),
    }
"""
            )
        else:
            f.write(
                """import json
from dataclasses import dataclass
import os
import boto3

# TODO: Remove this todo, uncomment the dataclasses and add the correct fields for Input and Output

# @dataclass
class Input:
    pass


# @dataclass
class Output:
    pass


def lambda_handler(event: Input, context) -> Output:
    dynamodb = boto3.resource("dynamodb")
    CONTROL_TABLE_NAME = os.environ.get("CONTROL_TABLE_NAME")
    control_table = dynamodb.Table(CONTROL_TABLE_NAME)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello World!"}),
    }
"""
            )

    with open("infra/stacks/lambda_stack.py", "r") as f:
        lines = f.readlines()
        index = lines.index("from infra.services import Services\n") - 2

        lines.insert(
            index,
            f"from {folder_path.replace('/','.')}.config import {config}\n",
        )

        comment = "".join(word.capitalize() for word in comment.split("_"))

        try:
            comment_index = lines.index(f"        # {comment}\n")
            lines.insert(comment_index + 1, f"        {config}(self.services)\n")
        except:
            lines.append(f"\n")
            lines.append(f"        # {comment}\n")
            lines.append(f"        {config}(self.services)\n")

    with open("infra/stacks/lambda_stack.py", "w") as f:
        for line in lines:
            f.write(line)


if __name__ == "__main__":
    gaia()
