# kdtree algorithm
"""

Reference:
[1] https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/kdtrees.pdf

"""
from numpy import median
from heapq import *

class Node(object):
    def __init__(self, val, left=None, right=None):
        
        self.val = val 
        self.left = left
        self.right = right
    
    def __str__(self) -> str:
        return f"val: {self.val}, left: [{self.left}], right: [{self.right}]"

def get_k_median(arr, axi):
    arr.sort(key = lambda x: x[axi])
    return len(arr)//2

def get_distance(target, nodeval):
    # L1 distance or blocker distance
    dis = sum([abs(t - q) for t, q in zip(target, nodeval)])
    return dis

class kdtree(object):

    def __init__(self, elemlist) -> None:
    
        self.dim = len(elemlist[0])
        self.locations = self.construct(elemlist=elemlist,
                                        depth=0)
    
    def __str__(self) -> str:
        return "location {}".format(self.locations)

    def construct(self, elemlist, depth):
        if not elemlist: return None

        axis = depth % self.dim 

        pos = get_k_median(elemlist, axis)

        left = self.construct(elemlist[:pos], depth + 1)
        right = self.construct(elemlist[pos+1:], depth+1)
        node = Node(elemlist[pos], left, right)

        return node

    def search(self, target, topk=1, bbox=3):
        assert self.locations is not None

        self.mdist = []

        def _search(node, target, axis, topk):
            if node is None: return

            axis = axis % self.dim

            val = target[axis]
            if val < node.val[axis]:
                _search(node.left, target, axis + 1, topk=topk)
                if val + bbox > node.val[axis]:
                    _search(node.right, target, axis + 1, topk=topk)
            else:
                _search(node.right, target, axis + 1, topk=topk)
                if val - bbox < node.val[axis]:
                    _search(node.left, target, axis + 1, topk=topk)

            dis = get_distance(target, node.val)
            if len(self.mdist) == 0:
                self.mdist.append((dis, node.val))
            else:
                if dis < self.mdist[0][0]:
                    self.mdist.insert(0, (dis, node.val))

        _search(self.locations, target, 0, topk)

        return f"distance: {self.mdist[0][0]}, location: {self.mdist[0][1]}"
    
def main():
    """Example usage of kdtree"""
    point_list = [(7, 2), (5, 4), (9, 6), (4, 7), (8, 1), (2, 3)]
    tree = kdtree(point_list)
    print(tree)

def city_houses():
    """
    Here we compute the distance to the nearest city from a list of N cities.
    The first line of input contains N, the number of cities.
    Each of the next N lines contain two integers x and y, which locate the city in (x,y),
    separated by a single whitespace.
    It's guaranteed that a spot (x,y) does not contain more than one city.
    The output contains N lines, the line i with a number representing the distance
    for the nearest city from the i-th city of the input.
    """
    """
    n = int(input())
    cities = []
    for i in range(len(cities)):
        city = i, tuple(map(int, input().split(' ')))
        cities.append(city)
    # print(cities)
    """
    cities = [(7, 2), (5, 4), (9, 6), (4, 7), (8, 1), (2, 3)]

    target = (2, 5)
    tree = kdtree(cities)
    # print(tree)
    ans = tree.search(target)
    print(ans)

def distance(a, b):
    # Taxicab distance is used below. You can use squared euclidean distance if you prefer
    k = len(b)
    total = 0
    for i in range(k):
        total += abs(b[i] - a[i])
    return total


if __name__ == '__main__':
    main()
    city_houses()

