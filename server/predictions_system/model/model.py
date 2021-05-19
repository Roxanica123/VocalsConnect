class Model:
    def __init__(self, input_shape, output_size, load_path_weights=None, optimizer_learning_rate=0.001):
        self.input_shape = input_shape
        self.output_size = output_size
        self.load_path_weights = load_path_weights
        self.optimizer_learning_rate = optimizer_learning_rate
        self.model = self.build_model()
        if self.load_path_weights is not None:
            self.model.load_weights(self.load_path_weights).expect_partial()
            print("Loaded weights")

    def build_model(self, *args, **kwargs):
        return None

    def predict(self, x_predict):
        return self.model.predict(x_predict, verbose=1)
