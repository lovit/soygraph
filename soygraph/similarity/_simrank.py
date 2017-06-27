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
    def __init__(self, graph, max_iter=10, decaying_factor=0.80):
        self.g = graph
        self.max_iter = max_iter
        self.df = decaying_factor
        normalizer=lambda x: sum([w for node, w in x])
        self.normi = {n:normalizer(inbs) for n, inbs in self.g.inb.items()}
        self.normo = {n:normalizer(outbs) for n, outbs in self.g.outb.items()}
        
    def query(self, q, topk=10, max_iter=-1):
        if max_iter < 0:
            max_iter = self.max_iter
        tops = {q:1}
        sims = {q:1}
        kth = 0
        
        for n_iter in range(1, max_iter+1):
            df = pow(self.df, n_iter)
            
            sorted_sim = sorted(sims.items(), key=lambda x:x[1], reverse=True)
            kth = sorted_sim[:topk][-1][1]
            delta = (kth - sorted_sim[:topk+1][-1][1])
            if delta > df:
                break
            
            tops_ = {}
            btrks = {}
            for topb, tbw in tops.items():
                for inb, inbw in self.g.inbounds(topb):
                    inbw /= self.normi[topb]
                    tops_[inb] = (tops_.get(inb, 0) + tbw * inbw)
                    btrks[topb] = (btrks.get(topb, 0) - tbw * inbw)
                    
            for top, tw in tops_.items():
                for outb, outbw in self.g.outbounds(top):
                    outbw /= self.normi[outb]
                    if outbw < delta:
                        continue
                    btrks[outb] = (btrks.get(outb, 0) + tw * outbw)
            
            btrks = {n:w for n,w in btrks.items() if w > 0}
            tops = tops_
            if not btrks:
                continue
                    
            for n_back in range(1, n_iter):                
                btrks_ = {}
                for top, tw in btrks.items():
                    for outb, outbw in self.g.outbounds(top):
                        outbw /= self.normi[outb]
                        btrks_[outb] = (btrks_.get(outb, 0) + tw * outbw)
                btrks = btrks_
            
            for launch, lw in btrks.items():
                if q != launch:
                    sims[launch] = sims.get(launch, 0) + lw * df
        del sims[q]
        return sims


class SinglePairSimRank:
    def __init__(self, graph, max_iter=10, decaying_factor=0.85):
        self.g = graph
        self.max_iter = max_iter
        self.df = decaying_factor

    def query(self, q1, q2):
        sim = 0
        # TODO
        return sim
