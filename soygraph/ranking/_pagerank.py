class PageRank:
    def __init__(self, graph=None, max_iter=10, decaying_factor=0.85, bias=None):
        self.g = graph
        self.max_iter = max_iter
        self.df = decaying_factor
        self.b = bias
        self.rank = {}

    def train(self, graph=None, bias=None):
        if graph:
            self.g = graph
        if bias:
            self.b = bias

        # TODO
        return self.rank

    def iterate(self):
        # TODO
        return self.rank 