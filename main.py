from lib.Stream import Stream
from lib.TimeNode import TimeNode, TimeNodeSet
import torch

def loss():
    pass

class Stream2Vec():

    def __init__(self, s):
        self.embs = {}
        self.s = s

    def update_time(self, node, link):

        sub_W = TimeNodeSet(elements=[ TimeNode(x, link["b"], link["e"]) for x in s.V ])
        subs = self.s.substream(sub_W, sub_W)

        embs_time = [ self.embs[v] for v in subs.V ] + [self.embs[node]]

        return torch.mean(torch.stack(embs_time), dim=0)


    def embeddings(self, d=3, K=1):
        """
            Returns embeddings for all nodes in s.V
        """
        self.embs = { v: torch.rand(d) for v in self.s.nodes() }

        for k in range(0, K):
            for l in self.s.E:
                u, v, b, e = l["u"], l["v"], l["b"], l["e"]
                self.embs[u] = self.update_time(u, l)
                self.embs[u] = self.update_graph(u, l)
                self.embs[u] = self.update_node(u, l)

                self.embs[v] = self.update_time(v, l)
                self.embs[v] = self.update_graph(v, l)
                self.embs[v] = self.update_node(v, l)
        
        return self.embs


# ------ MAIN ------
s = Stream()
s.readStream("data/dummy/test.json")
model = Stream2Vec(s)
embeds = model.embeddings()
print(embeds)
