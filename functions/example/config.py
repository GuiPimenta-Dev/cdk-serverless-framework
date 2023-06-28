from infra.services import Services


class ExampleConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="ExampleFunction",
            path="./functions/example",
            description="An example function",
        )

        services.api_gateway.create_endpoint("POST", "/examples/{example_id}", function)
