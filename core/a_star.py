import queue
import math
class NodePath:
    def __init__(self, path):
        self._path = []
        if isinstance(path, list):
            self._path = path
        else:
            self.add(path)

    def get_path(self):
        return self._path

    def add(self, node):
        self._path.append(node)

    def count(self):
        return len(self._path)

    def get_path_cost(self):
        total_f = 0
        for node in self._path:
            total_f = node.get_f() + total_f
        return total_f

    def __eq__(self, other):
        return self.get_path_cost() == other.get_path_cost()

    def __lt__(self, other):
        return self.get_path_cost() < other.get_path_cost()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self._path)


class Node:
    def __init__(self, grid_position, is_accessible=True):
        self._h = 0
        self._g = 0
        self._grid_position = grid_position
        self._is_accessible = is_accessible

    def get_position(self):
        return self._grid_position

    def get_f(self):
        return self._g + self._h

    def calc_heuristic(self, destination_node):
        diff_position = (destination_node.get_position()[0] - self.get_position()[0],
                         destination_node.get_position()[1] - self.get_position()[1])
        self._h = math.sqrt((diff_position[0]) ** 2 + (diff_position[1]) ** 2)

    def set_weighting(self, g):
        self._g = g

    def set_accessibility(self, accessibility):
        self._is_accessible = accessibility

    def reset(self):
        self._h = 0
        self._g = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Node[{}, {}]".format(self._grid_position[0], self._grid_position[1])

    def __eq__(self, other):
        if isinstance(other, Node):
            if self.get_position() == other.get_position():
                return True
        return False


class Grid:
    def __init__(self, grid_size):
        self._grid_size = grid_size
        self._nodes = [[Node((x, y)) for x in range(self._grid_size[0])] for y in range(self._grid_size[1])]

    def get_node(self, position):
        if position[0] >= self._grid_size[0] or position[1] >= self._grid_size[1]:
            raise Exception("position out of bound")
        return self._nodes[position[1]][position[0]]

    def get_path(self, start_node, destination_node, open_nodes=[], closed_nodes=[]):
        path = self._calculate_path(start_node, destination_node, open_nodes, closed_nodes)
        for node in open_nodes + closed_nodes:
            node.reset()
        return path

    def _calculate_path(self, start_node, destination_node, open_nodes=[], closed_nodes=[]):
        if start_node == destination_node:
            return NodePath(start_node)

        relative_neighbor_positions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        node_path_queue = queue.PriorityQueue()
        node_path_queue.put(NodePath(start_node))

        while node_path_queue.qsize() > 0:
            node_path = node_path_queue.get()
            node_list = node_path.get_path()
            last_node = node_list[-1]

            if last_node == destination_node:
                return node_path

            closed_nodes.append(last_node)

            for rnp in relative_neighbor_positions:
                neighbor_pos = (last_node.get_position()[0] + rnp[0], last_node.get_position()[1] + rnp[1])
                if neighbor_pos[0] < 0 or neighbor_pos[1] < 0 or neighbor_pos[0] >= self._grid_size[0] or neighbor_pos[1] >= self._grid_size[1]:
                    continue
                neighbor_node = self.get_node(neighbor_pos)
                if not neighbor_node._is_accessible or neighbor_node in open_nodes or neighbor_node in closed_nodes:
                    continue

                neighbor_node.calc_heuristic(destination_node)
                neighbor_node.set_weighting(1)

                open_nodes.append(neighbor_node)

                new_node_list = list(node_list)
                new_node_list.append(neighbor_node)
                node_path_queue.put(NodePath(new_node_list))

##############
# How to use #
##############

# size = (300, 300)
# grid = Grid(size)

# location_a = (20, 2)
# location_b = (10, 10)

# grid.get_node((15, 5)).set_accessibility(False) # set as "wall"
# ret = grid.get_path(grid.get_node(location_a), grid.get_node(location_b))
# print(ret.count())
# print(ret)
