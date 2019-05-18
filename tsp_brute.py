""" Simple TSP Bruteforce implementation
"""

import copy
import math
import time
import itertools
from tsp_utils import read_tsp, plot_tsp, route_distance


def solve(cities):
    """ Tries to find solution using Nearest Neighbor strategy

        Args:
            cities (dict): {city_index: {"x": xvalue, "y": yvalue}, ...}
    """

    best_route = list(cities.keys())
    best_distance = route_distance(cities, best_route)

    all_cities = list(cities.keys())

    print_index = 0

    for route in itertools.permutations(all_cities, len(all_cities)):
        distance = route_distance(cities, route)

        if distance < best_distance:
            best_distance = distance
            best_route = route

            print_index += 1

            plot_tsp(cities,
                     route,
                     str(distance),
                     show=False,
                     save=True,
                     filename="brute/{i}.png".format(i=print_index))

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
