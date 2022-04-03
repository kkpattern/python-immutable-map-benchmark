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


def benchmark_construct(input_map):
    print("Construct")
    print("Input map size: {0}".format(len(input_map)))
    number = 1000
    benchmark_globals = globals()
    benchmark_globals["input_map"] = input_map
    pyrsistent_cost = timeit.timeit(
        "a = construct_map_pyrsistent(input_map)",
        number=number,
        globals=benchmark_globals)
    print(f"pyrsistent cost {pyrsistent_cost}")
    frozendict_cost = timeit.timeit(
        "a = construct_map_frozendict(input_map)",
        number=number,
        globals=benchmark_globals)
    print(f"frozendict cost {frozendict_cost}")
    immutables_cost = timeit.timeit(
        "a = construct_map_immutables(input_map)",
        number=number,
        globals=benchmark_globals)
    print(f"immutables cost {immutables_cost}")


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


def update_and_diff_pyrsistent(map_, update_list):
    evolver = map_.evolver()
    for object_id, key_to_update, value_to_update in update_list:
        evolver[object_id] = evolver[object_id].set(key_to_update,
                                                    value_to_update)
    new_map = evolver.persistent()

    dirty_objects = {}
    for id_, object_ in new_map.items():
        if object_ is not map_.get(id_, None):
            dirty_objects[id_] = object_
    assert len(dirty_objects) == len(update_list)


def update_and_diff_frozendict(map_, update_list):
    raw_dict = dict(map_)
    for object_id, key_to_update, value_to_update in update_list:
        raw_dict[object_id] = raw_dict[object_id].set(key_to_update,
                                                      value_to_update)
    new_map = frozendict(raw_dict)

    dirty_objects = {}
    for id_, object_ in new_map.items():
        if object_ is not map_.get(id_, None):
            dirty_objects[id_] = object_
    assert len(dirty_objects) == len(update_list)


def update_and_diff_immutables(map_, update_list):
    evolver = map_.mutate()
    for object_id, key_to_update, value_to_update in update_list:
        evolver[object_id] = evolver[object_id].set(key_to_update,
                                                    value_to_update)
    new_map = evolver.finish()

    dirty_objects = {}
    for id_, object_ in new_map.items():
        if object_ is not map_.get(id_, None):
            dirty_objects[id_] = object_
    assert len(dirty_objects) == len(update_list)


def update_and_diff_case(map_size, change_size):
    assert map_size >= change_size
    print("Update and diff")
    print(f"map size: {map_size}")
    print(f"change size: {change_size}")
    benchmark_globals = globals()

    update_list = []
    for i in range(change_size):
        update_list.append((i, "name", f"new_name_{i}"))
    benchmark_globals["update_list"] = update_list

    id_to_object_raw = {}
    for i in range(map_size):
        id_to_object_raw[i] = pmap({"name": f"name{i}"})
    input_map = pmap(id_to_object_raw)
    benchmark_globals["input_map"] = input_map
    pyrsistent_cost = timeit.timeit(
        "update_and_diff_pyrsistent(input_map, update_list)",
        number=1000,
        globals=benchmark_globals)
    print(f"pyrsistent cost {pyrsistent_cost}")

    id_to_object_raw = {}
    for i in range(map_size):
        id_to_object_raw[i] = frozendict({"name": f"name{i}"})
    input_map = frozendict(id_to_object_raw)
    benchmark_globals["input_map"] = input_map
    frozendict_cost = timeit.timeit(
        "update_and_diff_frozendict(input_map, update_list)",
        number=1000,
        globals=benchmark_globals)
    print(f"frozendict cost {frozendict_cost}")

    id_to_object_raw = {}
    for i in range(map_size):
        id_to_object_raw[i] = Map({"name": f"name{i}"})
    input_map = Map(id_to_object_raw)
    benchmark_globals["input_map"] = input_map
    immutables_cost = timeit.timeit(
        "update_and_diff_immutables(input_map, update_list)",
        number=1000,
        globals=benchmark_globals)
    print(f"immutables cost {immutables_cost}")


def main():
    for case in [benchmark_construct,
                 benchmark_access,
                 benchmark_set,
                 benchmark_remove]:
        for size in [10, 100, 1000, 10000, 100000]:
            input_map = {}
            for i in range(size):
                input_map[f"key{i}"] = i
            case(input_map)
    for map_size in [1000, 10000]:
        # for change_size in [1, 10, 100]:
        for change_size in [1, 100, 1000]:
            update_and_diff_case(map_size, change_size)


if __name__ == "__main__":
    main()
