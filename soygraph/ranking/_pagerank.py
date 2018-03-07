class PageRank:
    def __init__(self, damping_factor=0.85, max_iter=10,
        converge_error=0.001, verbose=0, sum_weight=100):

        self.df = damping_factor
        self.max_iter = max_iter
        self.converge_error = converge_error
        self.verbose = verbose
        self.sum_weight = sum_weight

    def rank(self, graph, bias=None, is_normalized=True):
        if not is_normalized:
            graph, bias = self._type_check(graph, bias)

        if not bias:
            bias = {}

        N = graph.shape()[0] # number_of_nodes
        dw = self.sum_weight / N
        rank = {node:dw for node in range(N)}

        for num_iter in range(1, self.max_iter + 1):
            rank_ = self._update(rank, graph, bias, dw, self.df, N)
            diff = sum((abs(w - rank[n]) for n, w in rank_.items()))
            rank = rank_

            if diff < self.sum_weight * self.converge_error:
                if self.verbose:
                    print('\riter = %d Early stopped.' % num_iter, end='', flush=True)
                break

            if self.verbose:
                print('\riter = %d' % num_iter, end='', flush=True)

        if self.verbose:
            print('\rdone')

        return rank

    def _type_check(self, graph, bias):
        # TODO outbound normalize
        return graph, bias

    def _update(self, rank, graph, bias, dw, df, N):
        rank_new = {}
        df_ = 1 - df
        for to_node in range(N):
            inbounds = graph.inbounds(to_node)
            if not inbounds:
                rank_new[to_node] = 0
                continue
            rank_new_to = sum([w * rank[from_node] for from_node, w in inbounds])
            rank_new[to_node] = df * rank_new_to + df_ * bias.get(to_node, dw)
        return rank_new