import queue
import math
class NodePath:
    """
    Represents a path of nodes.

    :param path: Initial path (optional). If provided, it should be a list of nodes.
    """

    def __init__(self, path):
        """
        Initializes a NodePath object.

        :param path: Initial path (optional). If provided, it should be a list of nodes.
        """
        self._path = []
        if isinstance(path, list):
            self._path = path
        else:
            self.add(path)

    def get_path(self):
        """
        Returns the path.

        :return: The path as a list of nodes.
        """
        return self._path

    def add(self, node):
        """
        Adds a node to the path.

        :param node: The node to add.
        """
        self._path.append(node)

    def count(self):
        """
        Returns the number of nodes in the path.

        :return: The number of nodes in the path.
        """
        return len(self._path)

    def get_path_cost(self):
        """
        Calculates and returns the total cost of the path.

        :return: The total cost of the path.
        """
        total_f = 0
        for node in self._path:
            total_f = node.get_f() + total_f
        return total_f

    def __eq__(self, other):
        """
        Checks if two NodePath objects have the same path cost.

        :param other: The other NodePath object to compare.
        :return: True if the path costs are equal, False otherwise.
        """
        return self.get_path_cost() == other.get_path_cost()

    def __lt__(self, other):
        """
        Checks if the path cost of this NodePath object is less than the path cost of another NodePath object.

        :param other: The other NodePath object to compare.
        :return: True if this path cost is less than the other path cost, False otherwise.
        """
        return self.get_path_cost() < other.get_path_cost()

    def __repr__(self):
        """
        Returns a string representation of the NodePath object.

        :return: A string representation of the NodePath object.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns a string representation of the path.

        :return: A string representation of the path.
        """
        return str(self._path)


class Node:
    """
    Represents a node in a grid.

    :param grid_position: The position of the node in the grid.
    :type grid_position: tuple
    :param is_accessible: Indicates if the node is accessible or not. Default is True.
    :type is_accessible: bool
    """

    def __init__(self, grid_position, is_accessible=True):
        self._h = 0
        self._g = 0
        self._grid_position = grid_position
        self._is_accessible = is_accessible

    def get_position(self):
        """
        Get the position of the node in the grid.

        :return: The position of the node.
        :rtype: tuple
        """
        return self._grid_position

    def get_f(self):
        """
        Calculate and get the total cost of the node (g + h).

        :return: The total cost of the node.
        :rtype: float
        """
        return self._g + self._h

    def calc_heuristic(self, destination_node):
        """
        Calculate the heuristic value (h) of the node based on the destination node.

        :param destination_node: The destination node.
        :type destination_node: Node
        """
        diff_position = (destination_node.get_position()[0] - self.get_position()[0],
                         destination_node.get_position()[1] - self.get_position()[1])
        self._h = math.sqrt((diff_position[0]) ** 2 + (diff_position[1]) ** 2)

    def set_weighting(self, g):
        """
        Set the weighting value (g) of the node.

        :param g: The weighting value.
        :type g: float
        """
        self._g = g

    def is_accessible(self):
        """
        Check if the node is accessible.

        :return: True if the node is accessible, False otherwise.
        :rtype: bool
        """
        return self._is_accessible

    def set_accessibility(self, accessibility):
        """
        Set the accessibility of the node.

        :param accessibility: The accessibility value.
        :type accessibility: bool
        """
        self._is_accessible = accessibility

    def reset(self):
        """
        Reset the node by setting the heuristic (h) and weighting (g) values to 0.
        """
        self._h = 0
        self._g = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Node[{}, {}]".format(self._grid_position[0], self._grid_position[1])

    def __eq__(self, other):
        """
        Check if the node is equal to another node.

        :param other: The other node to compare.
        :type other: Node
        :return: True if the nodes are equal, False otherwise.
        :rtype: bool
        """
        if isinstance(other, Node):
            if self.get_position() == other.get_position():
                return True
        return False


class Grid:
    """
    Represents a grid of nodes for pathfinding.

    :param grid_size: The size of the grid (width, height).
    :type grid_size: tuple
    """

    def __init__(self, grid_size):
        """
        Initializes a Grid object.

        :param grid_size: The size of the grid (width, height).
        :type grid_size: tuple
        """
        self._grid_size = grid_size
        self._nodes = [[Node((x, y)) for x in range(self._grid_size[0])] for y in range(self._grid_size[1])]

    def get_node(self, position):
        """
        Retrieves the node at the specified position.

        :param position: The position of the node (x, y).
        :type position: tuple
        :return: The node at the specified position.
        :rtype: Node
        :raises Exception: If the position is out of bounds.
        """
        if position[0] >= self._grid_size[0] or position[1] >= self._grid_size[1]:
            raise Exception("position out of bound")
        return self._nodes[position[1]][position[0]]

    def get_path(self, start_node, destination_node, open_nodes=None, closed_nodes=None):
        """
        Calculates the path from the start node to the destination node.

        :param start_node: The starting node.
        :type start_node: Node
        :param destination_node: The destination node.
        :type destination_node: Node
        :param open_nodes: The list of open nodes. (optional)
        :type open_nodes: list, optional
        :param closed_nodes: The list of closed nodes. (optional)
        :type closed_nodes: list, optional
        :return: The path from the start node to the destination node.
        :rtype: NodePath

        Note:
            The open_nodes and closed_nodes parameters are optional and will be initialized as empty lists if not provided.
        """
        if open_nodes is None:
            open_nodes = []
        if closed_nodes is None:
            closed_nodes = []
        path = self._calculate_path(start_node, destination_node, open_nodes, closed_nodes)
        for node in open_nodes + closed_nodes + [start_node, destination_node]:
            node.reset()
        return path

    def _calculate_path(self, start_node, destination_node, open_nodes=None, closed_nodes=None):
        """
        Helper method to calculate the path from the start node to the destination node.

        :param start_node: The starting node.
        :type start_node: Node
        :param destination_node: The destination node.
        :type destination_node: Node
        :param open_nodes: The list of open nodes. (optional)
        :type open_nodes: list, optional
        :param closed_nodes: The list of closed nodes. (optional)
        :type closed_nodes: list, optional
        :return: The path from the start node to the destination node.
        :rtype: NodePath

        Note:
            The open_nodes and closed_nodes parameters are optional and will be initialized as empty lists if not provided.
        """
        if open_nodes is None:
            open_nodes = []
        if closed_nodes is None:
            closed_nodes = []
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