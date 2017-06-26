from ._pagerank import PageRank

class HITS(PageRank):
    def __init__(self, graph=None, max_iter=10, decaying_factor=0.85, bias=None):
    	super().__init__(graph, max_iter, decaying_factor, bias)

    def iterate(self):
        # TODO
        return self.rank 