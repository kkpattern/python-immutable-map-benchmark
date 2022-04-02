import copy
import timeit
from pyrsistent import pmap
from frozendict import frozendict
from immutables import Map


def construct_map_pyrsistent(input_map):
    map_ = pmap(input_map)
    return map_


def construct_map_frozendict(input_map):
    map_ = frozendict(input_map)
    return map_


def construct_map_immutables(input_map):
    map_ = Map(**input_map)
    return map_


def benchmark_access(input_map):
    print("Access")
    print("Input map size: {0}".format(len(input_map)))
    benchmark_globals = globals()
    benchmark_globals["input_map"] = input_map
    pyrsistent_cost = timeit.timeit(
        "a = map_[\"key2\"]",
        setup="map_ = construct_map_pyrsistent(input_map)",
        number=10000,
        globals=benchmark_globals)
    print(f"pyrsistent cost {pyrsistent_cost}")
    frozendict_cost = timeit.timeit(
        "a = map_[\"key2\"]",
        setup="map_ = construct_map_frozendict(input_map)",
        number=10000,
        globals=benchmark_globals)
    print(f"frozendict cost {frozendict_cost}")
    immutables_cost = timeit.timeit(
        "a = map_[\"key2\"]",
        setup="map_ = construct_map_immutables(input_map)",
        number=10000,
        globals=benchmark_globals)
    print(f"immutables cost {immutables_cost}")
    dict_cost = timeit.timeit(
        "a = map_[\"key2\"]",
        setup="map_ = copy.deepcopy(input_map)",
        number=10000,
        globals=benchmark_globals)
    print(f"builtin dict cost {dict_cost}")


def benchmark_set(input_map):
    print("Set")
    print("Input map size: {0}".format(len(input_map)))
    benchmark_globals = globals()
    benchmark_globals["input_map"] = input_map
    pyrsistent_cost = timeit.timeit(
        "a = map_.set(\"key2\", 0)",
        setup="map_ = construct_map_pyrsistent(input_map)",
        number=10000,
        globals=benchmark_globals)
    print(f"pyrsistent cost {pyrsistent_cost}")
    frozendict_cost = timeit.timeit(
        "a = map_.set(\"key2\", 0)",
        setup="map_ = construct_map_frozendict(input_map)",
        number=10000,
        globals=benchmark_globals)
    print(f"frozendict cost {frozendict_cost}")
    immutables_cost = timeit.timeit(
        "a = map_.set(\"key2\", 0)",
        setup="map_ = construct_map_immutables(input_map)",
        number=10000,
        globals=benchmark_globals)
    print(f"immutables cost {immutables_cost}")
    dict_cost = timeit.timeit(
        "map_[\"key2\"] = 0",
        setup="map_ = copy.deepcopy(input_map)",
        number=10000,
        globals=benchmark_globals)
    print(f"builtin dict cost {dict_cost}")


def benchmark_remove(input_map):
    print("Remove")
    print("Input map size: {0}".format(len(input_map)))
    benchmark_globals = globals()
    benchmark_globals["input_map"] = input_map
    pyrsistent_cost = timeit.timeit(
        "a = map_.remove(\"key2\")",
        setup="map_ = construct_map_pyrsistent(input_map)",
        number=10000,
        globals=benchmark_globals)
    print(f"pyrsistent cost {pyrsistent_cost}")
    frozendict_cost = timeit.timeit(
        "a = map_.delete(\"key2\")",
        setup="map_ = construct_map_frozendict(input_map)",
        number=10000,
        globals=benchmark_globals)
    print(f"frozendict cost {frozendict_cost}")
    immutables_cost = timeit.timeit(
        "a = map_.delete(\"key2\")",
        setup="map_ = construct_map_immutables(input_map)",
        number=10000,
        globals=benchmark_globals)
    print(f"immutables cost {immutables_cost}")
    # dict_cost = timeit.timeit(
    #     "del map_[\"key2\"]",
    #     setup="map_ = copy.deepcopy(input_map)",
    #     number=10000,
    #     globals=benchmark_globals)
    # print(f"builtin dict cost {dict_cost}")


def main():
    for case in [benchmark_access, benchmark_set, benchmark_remove]:
        for size in [10, 100, 1000, 10000, 100000]:
            input_map = {}
            for i in range(size):
                input_map[f"key{i}"] = i
            case(input_map)


if __name__ == "__main__":
    main()
