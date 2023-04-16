# kdtree algorithm
from numpy import median
from heapq import *

class Node(object):
    def __call__(self, val, left=None, right=None, point=None):
        
        self.val = val 
        self.left = left
        self.right = right
        self.point = point

def get_k_median(arr, axi):
    arr.sort(key = lambda x: x[axi])
    return len(arr)//2

def get_distance(target, nodeval):
    dis = sum([(t - q)*(t - q) for t, q in zip(target, nodeval)])
    return dis

class kdtree(object):

    def __init__(self, elemlist) -> None:
    
        self.dim = len(elemlist[0])
        self.locations = self.construct(elemlist=elemlist,
                                        depth=0)
    
    def construct(self, elemlist, depth):
        if not elemlist: return None

        axis = depth % self.dim 

        pos = get_k_median(elemlist, axis)

        left = self._construct(elemlist[:pos], depth + 1)
        right = self._construct(elemlist[pos+1], depth+1)
        node = Node(elemlist[pos], left, right)

        return node

    def search(self, target, topk=1):
        assert self.locations is not None

        self.mdist = ()

        def _search(node, target, axis, topk):
            if node is None: return

            val = target[axis]
            if val < node.val[axis]:
                _search(node.left, target, topk=topk)
            else:
                _search(node.right, target, topk=topk)

            dis = get_distance(target, node.val)
            if dis < self.mdist[0]:
                self.mdist = (dis, node)

        return self.mdist[1]