class ModelGatewayError(RuntimeError):
    """Base class for controlled model gateway failures."""


class UnsupportedModelProviderError(ValueError):
    pass


class ModelProviderConfigurationError(ModelGatewayError):
    pass


class ModelProviderRequestError(ModelGatewayError):
    pass


class ModelProviderResponseError(ModelGatewayError):
    pass
