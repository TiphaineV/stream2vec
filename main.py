from lib.Stream import Stream
import torch

def embeddings(s, d=3, K=10):
    """
        Returns embeddings for all nodes in s.V
    """
    embs = { v: torch.rand(d) for v in s.nodes() }

    for k in range(0, K):
        for l in s.E:
            continue

    return embs


# ------ MAIN ------
s = Stream()
s.readStream("data/dummy/test.json")
embeds = embeddings(s)
