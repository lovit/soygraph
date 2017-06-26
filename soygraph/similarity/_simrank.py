class SimRank:
    def __init__(self, graph=None, max_iter=10, decaying_factor=0.85):
        self.g = graph
        self.max_iter = max_iter
        self.df = decaying_factor
        self.sim = {}

    def train(self, graph=None):
        if graph:
            self.g = graph
        # TODO
        return self.sim

class SingleVectorSimRank:
    def __init__(self, graph, max_iter=10, decaying_factor=0.85):
        self.g = graph
        self.max_iter = max_iter
        self.df = decaying_factor

    def query(self, q):
        sim = {}
        # TODO
        return sim


class SinglePairSimRank:
    def __init__(self, graph, max_iter=10, decaying_factor=0.85):
        self.g = graph
        self.max_iter = max_iter
        self.df = decaying_factor

    def query(self, q1, q2):
        sim = 0
        # TODO
        return sim
