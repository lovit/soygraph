class SimRank:
    def __init__(self, graph=None, max_iter=10, decaying_factor=0.85, 
                 min_similarity=0.005, max_norm=True, verbose=True):
        self.g = graph
        self.max_iter = max_iter
        self.df = decaying_factor
        self.sim = {}
        self.min_similarity = min_similarity
        self.max_norm = max_norm
        self.verbose = verbose

    def train(self, graph=None):
        if graph:
            self.g = graph
        
        if self.max_norm:
            norm = {n:max([w for inbn, w in inbs]) for n, inbs in self.g.inb.items()}
        else:
            norm = {n:sum([w for inbn, w in inbs]) for n, inbs in self.g.inb.items()}
        
        for n_iter in range(1, self.max_iter+1):
            sim_ = defaultdict(lambda: defaultdict(lambda: 0))
            for a in self.g.nodes():                
                for b in self.g.nodes():
                    if a == b: continue
                    inbs_a = self.g.inbounds(a) 
                    inbs_b = self.g.inbounds(b)                    
                    sim_ab = 0

                    for inb_a, w1 in inbs_a:
                        for inb_b, w2 in inbs_b:
                            sim_ab_ = self.sim.get(inb_a, {}).get(inb_b, 0) if inb_a != inb_b else 1.0          
                            sim_ab += sim_ab_ * w1 * w2
                    sim_ab *= (self.df / (len(inbs_b) * len(inbs_a) * norm[a] * norm[b]))
                    if sim_ab >= self.min_similarity:
                        sim_[a][b] = sim_ab

            self.sim = {n:dict(sv) for n, sv in sim_.items()}            
            if self.verbose:
                print('#iter = %d' % n_iter)                
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
