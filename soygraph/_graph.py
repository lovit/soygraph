class DictGraph:
    def __init__(self, graph=None):
        if graph and type(graph) == dict and type(list(graph.values())[0]) == dict:
            self._index(graph)

    def _index(self, graph):
        self.inb = defaultdict(lambda: [])
        for from_node, to_dict in graph.items():
            to_list = list(sorted(to_dict.items(), key=lambda x:x[1]))
            self.outb[from_node] = to_list
            for to_node, weight in to_list:
                self.inb[to_node].append((from_node, weight))
        self.inb = dict(self.inb)

    def load_graph(self, fname, delimiter='\t'):
        with open(fname, encoding='utf-8') as f:
            for row in f:
                row = row.strip().split(delimiter)
                if len(row) != 3:
                    print('Exception: %s' % row)
                    continue
                from_node, to_node, weight = row
                self.add_node(from_mode, to_node, float(weight))

    def save_graph(self, fname, delimiter='\t'):
        f = open(fname, encoding='utf-8')
        d = delimiter
        for from_node, to_list in self.outb.items():
            fn = str(from_node)
            for to_node, weight in to_list:
                tn = str(to_node)
                f.write('%s%s%s%s%f\n' % (fn, d, tn, d, weight))
        f.close()

    def inbounds(self, to_node):
        """It returns list of tuple. 
        [(from_node_1, weight), (from_node_2, weight), ...]
        """
        return self.inb.get(to_node, [])

    def outbounds(self, from_node):
        """It returns list of tuple. 
        [(to_node_1, weight), (to_node_2, weight), ...]
        """

        return self.outb.get(from_node, [])

    def add_node(self, from_node, to_node, weight):
        inbounds = self.inb.get(to_node, [])
        inbounds.append((from_node, weight))
        self.inb[to_node] = inbounds

        outbounds = self.outb.get(from_node, [])
        outbounds.append((to_node, weight))
        self.outb[from_node] = outbounds

    def nodes(self):
        """It returns actual existing vertex"""
        nodes = set(self.inb.keys())
        nodes.update(set(self.outb.keys()))
        return nodes

    def shape(self):
        """It returns (V, E)"""
        V = max(max(self.inb.keys()), max(self.outb.keys())) + 1
        E = sum([len(from_list) for to_node, from_list in self.outb.items()])
        return (V, E)