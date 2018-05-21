"""
A Star Algorithm related stuff module
"""

from math import inf
import shutil

from data_structures import Graph, PriorityQueue
from utils import parse_input_a_estrella, load_input, print_console
from utils import get_direction, write_output_file, format_path, check_root, check_folder


def heuristic(node_1, node_2):
    """ Heuristic when only 4 directions are posible (Manhattan) """
    (x_node_1, y_node_1) = node_1
    (x_node_2, y_node_2) = node_2
    return abs(x_node_1 - x_node_2) + abs(y_node_1 - y_node_2)


class AStar:
    """
    A star algorithm implementation class
    """

    def __init__(self, args=None, enviroment=None, app_root=""):
        self.args = args
        enviroment, graph = parse_input_a_estrella(
            load_input(self.args.tablero_inicial))
        self.enviroment = enviroment or {}  # Estado del (todo) ambiente
        self.graph = graph or Graph()  # Grafo de todo el ambiente

        self.app_root = format_path(app_root)
        self.folders = ["Output"]
        check_root(self.app_root, self.folders)

    def set_enviroment(self, enviroment):
        """
        Sets the enviroment variable
        """
        if enviroment:
            self.enviroment = enviroment
        else:
            raise ValueError(
                "enviroment variable must be a non-empty dictionary")

    def a_star_search(self, goal, accesible_nodes):
        """
        Backbone of the algorithm
        """
        initial = self.enviroment["bunny"]
        frontier = PriorityQueue()
        frontier.push(element=initial, priority=0)

        accumulated_cost = {initial: 0}
        paths = {}

        result = {}
        result[initial] = dict.fromkeys(accesible_nodes, inf)
        for key in accesible_nodes:
            result[key] = dict.fromkeys(accesible_nodes, inf)

        end = False
        while frontier:
            current = frontier.pop()

            if current == goal or end:
                break

            for node in self.graph.neighbors(current):
                if node in accesible_nodes:
                    # cost from current to neighbor = 1
                    current_cost = accumulated_cost[current] + 1
                    if node not in accumulated_cost or current_cost < accumulated_cost[node]:
                        accumulated_cost[node] = current_cost
                        # f(n) = g(n) + h(n)
                        priority = current_cost + heuristic(goal, node)
                        if self.graph.nodes[node].carrot:
                            priority = 0
                        result[current][node] = priority
                        paths[current] = node
                        frontier.push(element=node, priority=priority)
        return result, paths

    def get_neighbour_costs(self):
        """
        Obtains the cost of the neighbors
        """
        accesible_nodes = self.graph.get_scope_keys(
            self.enviroment["bunny"], self.args.vision)
        all_costs = {}
        all_min_costs = []
        for valid_node in self.graph.neighbors(
                self.enviroment["bunny"]):  # accesible_nodes:
            costs, path = self.a_star_search(valid_node, accesible_nodes)
            for node in path:
                min_cost = min(path, key=path.get)
                if path[min_cost] not in all_min_costs:
                    all_min_costs.append(path[min_cost])
            for node in self.graph.neighbors(self.enviroment["bunny"]):
                if node not in all_costs:
                    all_costs[node] = []
                all_costs[node].append(costs[self.enviroment["bunny"]][node])
        for node in all_costs:
            if node in all_min_costs:
                all_costs[node] = min(all_costs[node])
            else:
                all_costs[node] = sum(all_costs[node])
        return all_costs

    def step(self):
        """
        Step execution
        """
        # pprint(self.enviroment)
        current_pos = self.enviroment["bunny"]
        costs = self.get_neighbour_costs()

        best_cost = min(costs, key=costs.get)
        best_direction = get_direction(current_pos, best_cost)
        # Move bunny and eat if there is a carrot
        self.enviroment["bunny"] = best_cost
        if self.graph.nodes[best_cost].consume_carrot():
            self.enviroment["carrot"].remove(best_cost)
            self.args.zanahorias -= 1

        scores = {}
        for key in costs:
            direction = get_direction(current_pos, key)
            scores[direction] = costs[key]
        scores["MOVIMIENTO"] = best_direction
        return scores

    def check_enviroment(self):
        """ Checks that the enviroment is full of necesary variables"""
        enviromental_variables = ["bunny", "carrot", "size"]
        for key in enviromental_variables:
            if key not in self.enviroment:
                raise ValueError(key + " not present in the enviroment")
            value = self.enviroment[key]
            if not value:
                raise ValueError(key + "'s value must not be None")
            if not isinstance(value, list) and not isinstance(value, tuple):
                raise ValueError(key + "'s value must be a list or tuple")
            if isinstance(value, list) and not value:
                raise ValueError(key + "'s value must not be empty")

    def run(self):
        """
        Runs the algorithm
        """
        # Check that everything is fine with the enviroment
        self.check_enviroment()

        # Output directory for this run
        curr_out_dir = self.app_root + 'Output/AStar/'
        shutil.rmtree(curr_out_dir, ignore_errors=True)
        check_folder(curr_out_dir)
        print("OUTPUT DIRECTORY", curr_out_dir)
        # print(self.graph)
        step_no = 0
        maximum_steps = 20

        # Initial amount of carrots
        carrot_amount = len(self.enviroment["carrot"])

        # Initial state
        formated_step = format(step_no, '05d')
        write_output_file(
            formated_step,
            curr_out_dir,
            self.enviroment,
            self.args.debug)

        while True:
            formated_step = format(step_no, '05d')
            if carrot_amount < self.args.zanahorias:
                print("PASO:", formated_step, "FINAL")
                print("Menos zanahorias de las necesarias, imposible de terminar")
                break
            if self.args.zanahorias == 0:
                print("PASO:", formated_step, "FINAL")
                print("Conejo satisfecho!")
                break
            if step_no == maximum_steps:
                print("PASO:", formated_step, "FINAL")
                print("Maxima cantidad de pasos, imposible terminar")
                break
            scores = self.step()
            print_console(formated_step, scores)
            write_output_file(
                formated_step,
                curr_out_dir,
                self.enviroment,
                self.args.debug)

            step_no += 1
