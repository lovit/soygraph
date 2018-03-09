class RandomWalkwithRestart:
    def __init__(self, graph=None, max_iter=10,
        decaying_factor=0.85, bias=None):

        self.g = graph
        self.max_iter = max_iter
        self.df = decaying_factor
        self.b = bias
        self.sum_outb_weights = {node:sum(
            [w for _, w in graph.outbounds(node)])
            for node in graph.nodes()
        }

    def query(self, q, topk=-1, max_iter=-1, df=-1):
        max_iter = self.max_iter if max_iter < 0 else max_iter
        df = self.df if df < 0 else df

        norm = sum([pow(self.df, p) for p in range(1, max_iter+1)])
        frontiers, ranks = {q:1}, {}

        for n_iter in range(max_iter):
            print(frontiers.keys())
            frontiers_ = {q: 1-df}
            for frontier, fw in frontiers.items():
                for outb, outb_w in self.g.outbounds(frontier):
                    frontiers_[outb] = frontiers_.get(outb,0) + (
                        fw * outb_w * df / self.sum_outb_weights[frontier])
            for frontier, fw in frontiers_.items():
                ranks[frontier] = ranks.get(frontier,0) + fw
            frontiers = frontiers_

        ranks = {node:rank/norm for node, rank in ranks.items() if node is not q}
        ranks = sorted(ranks.items(), key=lambda x:-x[1])
        if topk > 0:
            ranks = ranks[:topk]

        return ranks