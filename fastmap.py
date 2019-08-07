import networkx
import random
import math


# k = max dimensions allowed in the euclidean embedding
# epsilon = threshold of diminishing returns (graph dist. b/w furthest pair of points negligible)
# d(i,j) = distance b/w vertices v(i) and v(j)

# graph G(V,E) = input graph G with V vertices and E edges
# input is: G(V,E); K; epsilon

# every iteration identifies furthest pair of vertices (v(a) and v(b)) in input graph G (near linear time)
# builds two shortest path trees rooted at v(a) and v(b) (gives all necessary graph distances)

# accept graph data, K and epsilon values
# iterate over K; r -> K
# select random vertex v(a)
# set v(b) equal to v(a)
# C is a constant
# iterate over C; t -> C


def fastmap(G, K, epsilon):
    _my_graph = networkx.Graph(G)
    _arbitrary_const = 10  # Arbitrary constant

    _num_nodes = _my_graph.number_of_nodes()
    # num_edges = g.number_of_edges()

    # V = []
    # E = []
    _distances_dict = {}
    _embedding_dict = {}

    # V is list of nodes
    # E is list of edges (not required)
    # D is a dict containing distances

    # p is embedding matrix, form is dict, keys are nodes 1 to n and
    # values are lists of size r-1 containing embeddings for that node

    # Check default values for p matrix with Prof.

    # for i in range(_num_nodes):
    #     V.append(0)  ######
    _nodelist = list(_my_graph)
    # V = list(g.nodes)

    for _r in range(1, K + 1):
        _a = random.choice(_nodelist).index()    # Wrong ?
        _b = _a
        _nodelist[_b] = _nodelist[_a]

        for _i in _nodelist:
            _distances_dict[_i] = [] * len(_nodelist)
            # D[a][i] = 0
            # D[a, V.index(i)] = 0
            # D[i, b] = 0

        for _t in range(0, _arbitrary_const):

            for _i in range(len(_nodelist)):
                _distances_dict[_a][_i], _ = networkx.single_source_dijkstra(_my_graph, _nodelist[_a], _nodelist[_i])

            _tempmax = 0
            _maxindex = 0
            _templist = []

            for _i in range(len(_nodelist)):
                _tempvar = _distances_dict[_a][_i] ^ 2
                _running_sum = 0

                for _j in range(1, _r):
                    _running_sum = _running_sum + ((_embedding_dict[_a][_j] - _embedding_dict[_i][_j]) ^ 2)

                _templist[_i] = _tempvar - _running_sum

            for _i in _templist:
                if _tempmax < _templist[_i]:
                    _tempmax = _templist[_i]
                    _maxindex = _templist.index(_i)
            _arbitrary_const = _maxindex

            # V[c] = k[maxindex]  # ??? V? Node change? Check again with Prof.

            _nodelist[_arbitrary_const] = _nodelist[_maxindex]  # This is correct, I think

            # V[c] = max[Vi]{Dai^2 - sum[j = 1 to r-1] (Pa(j) - Pi(j))^2 )}

            # HOW TO CONVERT THESE TYPES OF LINES???

            if _nodelist[_arbitrary_const] == _nodelist[_b]:
                break
            else:
                _nodelist[_b] = _nodelist[_a]
                _nodelist[_a] = _nodelist[_arbitrary_const]

        for _v in range(len(_nodelist)):
            _distances_dict[_a][_v], _ = networkx.single_source_dijkstra(_my_graph, _nodelist[_a], _nodelist[_v])
            _distances_dict[_v][_b], _ = networkx.single_source_dijkstra(_my_graph, _nodelist[_v], _nodelist[_b])
            _distances_dict[_a][_b] = _distances_dict[_a][_v] + _distances_dict[_v][_b]

        _distances_prime_dict = {}

        _tempvar = (_distances_dict[_a][_b] ^ 2)
        _running_sum = 0
        for _j in range(1, _r):
            _running_sum = _running_sum + ((_embedding_dict[_a][_j] - _embedding_dict[_b][_j]) ^ 2)
        _distances_prime_dict[_a][_b] = _tempvar - _running_sum

        # DPrime[a][b] = D[a][b]^2 - sum[j = 1 to r-1] ((Pa(j) - Pb(j))^2)
        # DPrime[a][b] = 0  ######
        # DPrime[a][i] = 0  ######
        # DPrime[i][b] = 0  ######

        if _distances_prime_dict[_a][_b] < epsilon:
            break

        for _v in range(_num_nodes):
            _running_sum_first = 0
            _running_sum_second = 0
            for _j in range(1, _r):
                _running_sum_first = _running_sum_first + ((_embedding_dict[_a][_j] - _embedding_dict[_v][_j]) ^ 2)
                _running_sum_second = _running_sum_second + ((_embedding_dict[_v][_j] - _embedding_dict[_b][_j]) ^ 2)

            _x1 = (_distances_dict[_a][_v] ^ 2)
            _x2 = (_distances_dict[_v][_b] ^ 2)

            _distances_prime_dict[_a][_v] = _x1 - _running_sum_first
            _distances_prime_dict[_v][_b] = _x2 - _running_sum_second

            # DPrime[a][v] = D[a][v]^2 - sum[j = 1 to r-1] ((Pa(j) - Pi(j))^2)
            # DPrime[v][b] = D[v][b]^2 - sum[j = 1 to r-1] ((Pi(j) - Pb(j))^2)

            # embedding_dict[v][r] = (distances_prime_dict[a][v] + _distances_dict[a][b] - distances_prime_dict[v][b])
            # / (2 * math.sqrt(distances_prime_dict[a][b]))

            _numerator = _distances_prime_dict[_a][_v] + _distances_dict[_a][_b] - _distances_prime_dict[_v][_b]
            _denominator = float(2 * math.sqrt(_distances_prime_dict[_a][_b]))
            _embedding_dict[_v][_r] = float(_numerator / _denominator)
    return _embedding_dict

