""" Simple TSP nearest neighbor implementation
"""

import copy
import math
import time
import random
from tsp_utils import read_tsp, plot_tsp, euclidean_distance, route_distance


def find_closest(route, cities):
    """
    """

    # Current (last) city
    origin = cities[route[-1]]

    min_index = None
    min_dist = None

    for target_index in cities.keys():
        if target_index in route:
            # Skip visited cities
            continue

        d = euclidean_distance(origin, cities[target_index])

        if not min_dist or (min_dist and d < min_dist):
            min_dist = d
            min_index = target_index

    return min_index


def solve(cities):
    """ Tries to find solution using Nearest Neighbor strategy

        Args:
            cities (dict): {city_index: {"x": xvalue, "y": yvalue}, ...}
    """
    route = [random.choice(list(cities.keys()))]

    while True:
        l = len(route)

        if l % 100 == 0:
            print("Iteration ", len(route))

        index = find_closest(route, cities)

        if not index:
            # Chain is complete
            break

        route.append(index)
        # print(route)

    # Come back to start, connect last city to the first
    route.append(route[0])

    return route


if __name__ == "__main__":

    cities = read_tsp("data/dj38.tsp")  # 6656 for DJ

    t = time.time()
    
    print("Solving: finding route")
    route = solve(cities)
    print(route)

    tdiff = time.time() - t
    print("Time taken (s)")
    print(tdiff)

    print("Calculating route distance")
    distance = route_distance(cities, route)
    print(distance)

    print("Plotting")
    plot_tsp(cities, route, distance)
