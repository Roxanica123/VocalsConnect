class FeatureFunction:
    def __init__(self, feature_function: any, arguments: dict, name: str, requires_to_list: bool = True):
        self.feature_function = feature_function
        self.arguments = arguments
        self.requires_to_list = requires_to_list
        self.name = name
