import math
import matplotlib.pyplot as plt

def route_distance(cities, route):
    """ Traverse route and calculate distance
        Args:
        cities (dict): {city_index: {"x": xvalue, "y": yvalue}, ...}
        route (list): list of city indices
    """
    distance = 0

    for (i1, i2) in zip(route, route[1:]):
        distance += euclidean_distance(cities[i1], cities[i2])

    return distance

def euclidean_distance(city1, city2):
    """ Returns euclidean distance
        Args:
            city1 (dict): {"x": xvalue, "y": yvalue}
            city2 (dict): {"x": xvalue, "y": yvalue}
        Returns:
            distance (float)
    """
    d = math.sqrt((city1["x"] - city2["x"])**2 + (city1["y"] - city2["y"])**2)
    return d


def read_tsp(path):
    """ Read and parse TSP from given file path
    Args:
        path (string): location of *.tsp file
    Returns:
        data (dict): {city_index: {"x": xvalue, "y": yvalue}, ...}
    """
    data = {}

    with open(path, "r") as f:

        # Specification block
        for line in f:
            if line.strip() == "NODE_COORD_SECTION":
                break

        # Data block
        for line in f:
            line = line.strip()
            if line == "EOF":
                # End of data block
                break

            try:
                index, y, x = line.split(" ")
                data[int(index)] = {"x": float(x), "y": float(y)}
            except Exception as e:
                print(e)
                print("Can't parse data [{line}]")

        return data


def plot_tsp(cities, route=None, distance=None, filename="tsp.png", show=True, save=True):
    """ TSP Plotter
        Args:
            cities (dict): {city_index: {"x": xvalue, "y": yvalue}, ...}
            route (list): sequence of city indices
    """

    plt.figure(figsize=(10, 10))
    plt.axis("off")

    # Cities
    plt.scatter([c["x"] for c in cities.values()], 
                [c["y"] for c in cities.values()], 
                color="red", s=4)

    # Route
    if route:
        xs = []
        ys = []

        for city_index in route:
            xs.append(cities[city_index]["x"])
            ys.append(cities[city_index]["y"])

        plt.plot(xs, ys, color="green")

    if distance:
        plt.title("Distance: {distance}".format(distance=distance))

    # Actions
    if save:
        plt.savefig(filename)

    if show:
        plt.show()

    plt.close()
