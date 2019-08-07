import typing
import d3m.container
from d3m.primitive_interfaces.base import CallResult, MultiCallResult
from d3m.primitive_interfaces.base import *
import d3m.metadata.hyperparams as hyperparams

__all__ = ('TransformerPrimitiveBase',)

Inputs = d3m.container.DataFrame
Outputs = d3m.container.DataFrame


class fastmap_hyperparams(hyperparams.Hyperparams):
    dimension = UniformInt(lower=1, upper=20, upper_inclusive=True, default=10,
                           description="Number of dimensions for Fastmap algorithm",
                           semantic_types=["http://schema.org/Integer", "https://metadata.datadrivendiscovery.org/types/TuningParameter"])

    threshold = UniformInt(lower=10, upper=500, upper_inclusive=True, default=100,
                           description="Number of dimensions for Fastmap algorithm",
                           semantic_types=["http://schema.org/Integer", "https://metadata.datadrivendiscovery.org/types/TuningParameter"])

class Fastmap(PrimitiveBase[Inputs, Outputs, None, Hyperparams]):


    """
    A base class for primitives which are not fitted at all and can
    simply produce (useful) outputs from inputs directly. As such they
    also do not have any state (params).

    This class is parameterized using only three type variables, ``Inputs``,
    ``Outputs``, and ``Hyperparams``.
    """

    def __init__(self, *, hyperparams: fastmap_hyperparams) -> None:
        super(Fastmap, self).__init__(hyperparams=hyperparams)


def set_training_data(self) -> None:  # type: ignore
    """
    A noop.

    Parameters
    ----------
    """

    return

def fit(self, *, timeout: float = None, iterations: int = None) -> CallResult[None]:
    """
    A noop.
    """

    return CallResult(None)

def get_params(self) -> None:
    """
    A noop.
    """

    return None

def set_params(self, *, params: None) -> None:
    """
    A noop.
    """

    return

def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> CallResult[Output]:

    return None

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
        _a = random.choice(_nodelist).index()  # Wrong ?
        _b = _a
        _nodelist[_b] = _nodelist[_a]

        for _i in _nodelist:
            _distances_dict[_i] = [] * len(_nodelist)
            # D[a][i] = 0
            # D[a, V.index(i)] = 0
            # D[i, b] = 0

        for _t in range(0, _arbitrary_const):

            for _i in range(len(_nodelist)):
                _distances_dict[_a][_i], _ = networkx.single_source_dijkstra(_my_graph, _nodelist[_a],
                                                                             _nodelist[_i])

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
                _running_sum_second = _running_sum_second + (
                            (_embedding_dict[_v][_j] - _embedding_dict[_b][_j]) ^ 2)

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

def fit_multi_produce(self, *, produce_methods: typing.Sequence[str], inputs: Inputs, timeout: float = None,
                      iterations: int = None) -> MultiCallResult:  # type: ignore
    """
    A method calling ``fit`` and after that multiple produce methods at once.

    Parameters
    ----------
    produce_methods : Sequence[str]
        A list of names of produce methods to call.
    inputs : Inputs
        The inputs given to all produce methods.
    timeout : float
        A maximum time this primitive should take to both fit the primitive and produce outputs
        for all produce methods listed in ``produce_methods`` argument, in seconds.
    iterations : int
        How many of internal iterations should the primitive do for both fitting and producing
        outputs of all produce methods.

    Returns
    -------
    MultiCallResult
        A dict of values for each produce method wrapped inside ``MultiCallResult``.
    """

    return self._fit_multi_produce(produce_methods=produce_methods, timeout=timeout, iterations=iterations,
                                   inputs=inputs)
