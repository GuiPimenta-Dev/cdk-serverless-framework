from aws_cdk import aws_secretsmanager as secrets_manager


class SecretsManager:
    def __init__(self, scope) -> None:

        self.authorizer_secret = secrets_manager.Secret.from_secret_complete_arn(
            scope,
            id="AuthorizerSecret",
            secret_complete_arn="",
        )
