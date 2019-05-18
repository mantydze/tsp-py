import copy
import time
import random
from tsp_utils import read_tsp, plot_tsp, route_distance


class Route(object):
    def __init__(self):
        self.route = []
        self.distance = 0

    def init_random(self, cities):
        self.route = list(cities.keys())
        random.shuffle(self.route)
        self.route.append(self.route[0])  # go back to start

    def set_route(self, route):
        self.route = route

    def swap_cities(self, n_cities=1):
        """ Mutate route. Swap one or more cities.
            Do not affect start and end of the route

            Args:
                n (int): number or cities to swap

            Returns:
                route (Route): new instance of route
        """

        route = Route()
        route.set_route(self.route[:])

        for _ in range(random.randint(1, n_cities)):
            index1 = random.randint(1, len(self.route)-2)
            index2 = random.randint(1, len(self.route)-2)

            route.route[index1], route.route[index2] = route.route[index2], route.route[index1]

        return route

    def shuffle_segment(self, segment_size=5):
        """ Mutate route. Shuffle cities within segment. 
            Do not affect start and end of the route

            Args:
                segment_size (int): how many cities to shuffle

            Returns:
                route (Route): new instance of route

            raise Exception if segment size is longer than route itself
        """

        route = Route()
        route.set_route(self.route[:])

        l = len(self.route)
        if segment_size >= l:
            raise Exception("Segment size cannot be longer than route")

        upper_max = l - segment_size

        # Calculate lower and upper indices of the segment
        lower_index = random.randint(1, upper_max - 1)
        upper_index = lower_index + segment_size

        # Chop segment from the route
        segment = self.route[lower_index:upper_index]

        random.shuffle(segment)

        # Put segment back into the route
        for i in range(segment_size):
            route.route[lower_index+i] = segment[i]

        return route

    def shift_segment(self, segment_size=5, shift=5):
        """ Mutate route. Shift route segment to right
            example: 
            segment [2, 3, 4] is shifted by 2 to right
            before [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            after  [1, 5, 6, 2, 3, 4, 7, 8, 9, 10]

            Args:
                segment_size (int): how many cities to shift
                shift (int):  how far to shift

            Returns:
                route (Route): new instance of route
                
            raise Exception if segment size + shift is longer than route itself
        """
        route = Route()
        route.set_route(self.route[:])

        l = len(self.route)
        if (segment_size + shift) >= l:
            raise Exception("Segment size + shift cannot be longer than route")

        upper_max = l - segment_size

        # Calculate lower and upper indices of the segment
        lower_index = random.randint(1, upper_max - 1)
        upper_index = lower_index + segment_size

        # Chop segment from the route
        segment = self.route[lower_index:upper_index]

        upper_max = l - (segment_size + shift)

        # Calculate lower and upper indices of the segment
        lower_index = random.randint(1, upper_max - 1)
        upper_index = lower_index + segment_size

        # start, shift, segment, end
        route.route = self.route[:lower_index] + self.route[upper_index:upper_index +
                                                            shift] + self.route[lower_index:upper_index] + self.route[upper_index+shift:]

        return route


class GA(object):
    def __init__(self):
        self.population = []
        self.cities = None

    def optimize(self, cities, n_generations=1000, population_size=400, max_segment_size=5, dir_name="tmp"):
        """ This is where optimization happens

            Args:
                cities (dict):
                n_generation (int): how long to train
                population_size (int): how many routes to try in one evolution
                max_segment_size (int): max segment size used in route shuffle and shift
                dir_name (str): path of a directory to store intermediate results
        """
        self.cities = cities

        # Initial population
        while len(self.population) < population_size:
            route = Route()
            route.init_random(cities)
            self.population.append(route)

        # Variables used for saving intermediate results
        print_index = 1
        print_distance = 0

        last_distance = 0
        max_patience = 1000
        patience = max_patience

        # Evolutions (Generations)
        i = 0
        while True:
            i += 1

            # Calculate fitness for all routes
            for route in self.population:
                route.distance = route_distance(cities, route.route)

            # Sort population by distance in ASCending order
            self.population = sorted(
                self.population, key=lambda x: x.distance, reverse=False)

            # Keep training while distance decrease even if number of generations is reached
            if i > n_generations:
                if last_distance == int(self.population[0].distance):
                    patience -= 1
                else:
                    patience = max_patience

            # Stop training if distance does not decrease for 1000 (max_patience) evolutions
            if patience <= 0:
                break

            # Print and save intermediate results
            if i % 100 == 0 or i == 1:
                print("Iteration", i)
                print(self.population[0].distance)

                # Save new image only if distance is lower than previous image
                if print_distance != self.population[0].distance:
                    title = "{distance} ({i})".format(
                        distance=self.population[0].distance, i=i)

                    plot_tsp(cities, self.population[0].route,
                             title,
                             show=False,
                             save=True,
                             filename="{dir_name}/{i}.png".format(
                        dir_name=dir_name,
                        i=print_index))

                    print_distance = self.population[0].distance
                    print_index += 1

            last_distance = int(self.population[0].distance)

            next_generation = []

            # Add best routes into next generation
            for route in self.population[:100]:
                next_generation.append(route)

                # Swap few cities
                mutated = route.swap_cities(1)
                next_generation.append(mutated)

                # Swap few cities
                mutated = route.swap_cities(5)
                next_generation.append(mutated)

                # Swap few cities
                mutated = route.swap_cities(10)
                next_generation.append(mutated)

                # Shuffle a segment
                mutated = route.shuffle_segment(
                    segment_size=random.randint(2, max_segment_size))
                
                if mutated:
                    next_generation.append(mutated)

                # Shuffle a segment
                mutated = route.shuffle_segment(
                    segment_size=random.randint(2, max_segment_size))
                if mutated:
                    next_generation.append(mutated)

                # Shift a segment
                mutated = route.shift_segment(
                    segment_size=random.randint(2, max_segment_size),
                    shift=random.randint(1, 10))
                if mutated:
                    next_generation.append(mutated)

                # Shift a segment
                mutated = route.shift_segment(
                    segment_size=random.randint(2, max_segment_size),
                    shift=random.randint(1, 20))
                if mutated:
                    next_generation.append(mutated)

            # Add random routes to fill missing population
            while len(self.population) < population_size:
                route = Route()
                route.init_random(cities)
                self.population.append(route)

            self.population = next_generation

        return self.population[0].route


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 3:
        print("Usage: python3 tsp_ga.py data_file output_dir")
        print("Usage: python3 tsp_ga.py dj38 tmp")
        exit()

    filename = sys.argv[1]
    dir_name = sys.argv[2]

    cities = read_tsp(filename)

    t = time.time()
    print("Solving: finding route")
    ga = GA()
    route = ga.optimize(cities, n_generations=2000,
                        population_size=500,
                        max_segment_size=5,
                        dir_name=dir_name)

    print(route)

    tdiff = time.time() - t
    print("Time taken (s)")
    print(tdiff)

    print("Calculating route distance")
    distance = route_distance(cities, route)
    print(distance)

    print("Plotting")
    plot_tsp(cities, route, distance, save=False)
