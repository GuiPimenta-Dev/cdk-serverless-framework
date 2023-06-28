from infra.services.api_gateway import APIGateway
from infra.services.aws_lambda import AWSLambda
from infra.services.dynamo_db import DynamoDB
from infra.services.layers import Layers
from infra.services.secrets_manager import SecretsManager
from infra.services.sns import SNS


class Services:
    def __init__(self, scope, stage, arns, alarms, versioning) -> None:
        self.sm = SecretsManager(scope)
        self.sns = SNS(scope)
        self.api_gateway = APIGateway(scope, stage, self.sm)
        self.aws_lambda = AWSLambda(scope, stage, self.sns, alarms, versioning)
        self.dynamo = DynamoDB(scope, arns)
        self.layers = Layers(scope)
