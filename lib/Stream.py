import sys
import ujson as json
import logging

class TimeNode:
    """
        For later refactoring
    """
    def __init__(self, _node, _b, _e, _label=set()):
        self.node = _node
        self.b = _b
        self.e = _e
        self.label = _label
        
    def __str__(self):
        return f"{self.node} [{self.b}, {self.e}]"

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, o):
        return  self.node == o.node\
                and self.b == o.b\
                and self.e == o.e
    def __hash__(self):
        return hash((self.node, self.b, self.e))
        
class Stream:
    def __init__(self, lang=set(), _loglevel=logging.DEBUG, _fp=sys.stdout):
        self.T = {}
        self.V = []
        self.W = {}
        self.E = {}
        
        # Store both degree view and links (times) view,
        # as the optimal view is different depending on the calculation
        self.degrees = {}
        self.times = {}
        
        self.logger = logging.getLogger()
        self.logger.setLevel(_loglevel)
    
    def nodes(self):
        return self.V
    
    def add_link(self, l):
        u = l["u"]
        v = l["v"]
        b = l["b"]
        e = l["e"]
        if "label_u" in l:
            label_u = l["label_u"]
        else:
            label_u = ""

        if "label_v" in l:
            label_v = l["label_v"]
        else:
            label_v = ""

        # Maintain temporal adjacency list 
        try:
            self.degrees[u].append((v, b, 1, label_u))
            self.degrees[u].append((v, e, -1, label_u))
        except KeyError:
            self.degrees[u] = [(v, b, 1, label_u), (v, e, -1, label_u)]

        try:
            self.degrees[v].append((u, b, 1, label_v))
            self.degrees[v].append((u, e, -1, label_v))
        except KeyError:
            self.degrees[v] = [(u, b, 1, label_v), (u, e, -1, label_v)]

        # Maintain interaction times for each pair of nodes (u,v)
        try:
            self.times[frozenset([u,v])].append((b, e, label_u, label_v))
        except KeyError:
            self.times[frozenset([u,v])] = [ (b, e, label_u, label_v) ]
    
    def add_links(self, links):
        self.E = links
        self.V = set()
        self.T = { "alpha": 0, "omega": 10 }
        
        for (i, link) in enumerate(links):
            self.V.add(link["u"])
            self.V.add(link["v"])
            
            u = link["u"]
            v = link["v"]
            b = link["b"]
            e = link["e"]
            label_u = link["label_u"]
            label_v = link["label_v"]
            
            try:
                self.degrees[u].append((v, b, 1, label_u))
                self.degrees[u].append((v, e, -1, label_u))
            except KeyError:
                self.degrees[u] = [(v, b, 1, label_u), (v, e, -1, label_u)]
                
            try:
                self.degrees[v].append((u, b, 1, label_v))
                self.degrees[v].append((u, e, -1, label_v))
            except KeyError:
                self.degrees[v] = [(u, b, 1, label_v), (u, e, -1, label_v)]
    
            try:
                self.times[frozenset([u,v])].append((b, e, label_u, label_v))
            except KeyError:
                self.times[frozenset([u,v])] = [ (b, e, label_u, label_v) ]
    
    def readStream(self, filepath):
        fp = open(filepath)
        data = json.load(fp)
        self.T = data["T"]
        self.V = data["V"]
        self.E = data["E"]
        
        for link in self.E:
            self.add_link(link)
        
        return data
    
    def writeStream(self):
        data = { "T": self.T, "V": self.V, "W": self.W, "E": self.E }
        
        json.dump(data, open("./out.json", "w+"))
    
    def substream(self, W1, W2):
        # W1, W2: [(u, b,e), (v, b',e'), etc.]
        # returns a substream induced by a subset of W.
        # Only return links etc. involving W1, W2, at their resp. times
        
        subs = Stream()
        subs.T = self.T
        subs.V = set([x[0] for x in  W1 ] + [x[0] for x in W2])
        subs.W = set(list(W1) + list(W2))
        subs.E = []
        subs.degrees = { u: [] for u in subs.V }
        
        for l in self.E:
            if l["u"] in subs.V and l["v"] in subs.V :
                subs.add_link(l)
                subs.E.append(l)
        
        return subs
    
    def neighbours(self, node):
        return set([ x[0] for x in self.degrees[node] ])
    
