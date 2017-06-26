class RandomWalkwithRestart:
    def __init__(self, graph=None, max_iter=10, decaying_factor=0.85, bias=None):
        self.g = graph
        self.max_iter = max_iter
        self.df = decaying_factor
        self.b = bias
        self.rank = {}