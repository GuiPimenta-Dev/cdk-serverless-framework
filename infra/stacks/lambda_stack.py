from aws_cdk import Stack
from constructs import Construct

from functions.example.config import ExampleConfig
from infra.services import Services


class LambdaStack(Stack):
    def __init__(
        self,
        scope: Construct,
        stage,
        arns,
        alarms=False,
        versioning=False,
        **kwargs,
    ) -> None:

        name = scope.node.try_get_context("name")
        super().__init__(scope, f"{name}CDK", **kwargs)

        self.services = Services(self, stage, arns, alarms, versioning)

        # Example
        ExampleConfig(self.services)
