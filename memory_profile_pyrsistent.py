from pyrsistent import pmap
from memory_profiler import profile


@profile
def main(input_map):
    map_ = pmap(input_map)
    history = []
    for i in range(1000):
        history.append(map_)
        map_ = map_.set(i, 0)


if __name__ == "__main__":
    input_map = {}
    for i in range(1000):
        input_map[i] = i
    main(input_map)
