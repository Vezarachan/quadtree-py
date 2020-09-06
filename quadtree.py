import os
from typing import List, Any, Union
import math


class Point(object):
    """
    Point class
    """
    x: float
    y: float
    data: Any

    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.data = data

    def __repr__(self):
        return '<Point: ({0},{1})>'.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Bounds(object):
    """
    BoundingBox
    """
    x: float
    y: float
    width: float
    height: float

    def __init__(self, x: float, y: float, width: float = 0, height: float = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        xmin, xmax, ymin, ymax = self.get_bbox()
        return '<Bounds: [{0},{1},{2},{3}]>'.format(xmin, xmax, ymin, ymax)

    def get_bbox(self):
        """
        retuen bbox: xmin, xmax, ymin, ymax
        :return List[int]:
        """
        return [self.x, self.x + self.width, self.y, self.y + self.height]
        
    def intersects(self, other):
        """
           Check is self Bounds intersects with another Bounds
           :param self:
           :param other:
           :return: bool
           """
        self_xmin = self.x
        self_xmax = self.x + self.width
        self_ymin = self.y
        self_ymax = self.y + self.height
        other_xmin = other.x
        other_xmax = other.x + other.width
        other_ymin = other.y
        other_ymax = other.y + other.height

        # self is left to another
        if self_xmax < other_xmin:
            return False
        # self is right to another
        if self_xmin > other_xmax:
            return False
        # self is above another
        if self_ymax < other_ymin:
            return False
        # self is below another
        if self_ymin > other_ymax:
            return False
        return True


def euclid_distance(one: Bounds, another: Union[Bounds, Point]) -> float:
    """
    calculate the euclid distance between two points or Bounds
    :param one:
    :param another:
    :return float:
    """
    return math.sqrt((one.x - another.x)**2 + (one.y - another.y)**2)


class QuadTree(object):
    """
    QuadTree - the quadtree data structure
    """
    __max_objects: int = 10
    __max_levels: int = 5
    __level: int
    __objects: List
    __bounds: Bounds
    __nodes: List
    __indices = []

    def __init__(self, bounds: Bounds, max_objects: int = 10, max_level: int = 4, level: int = 0):
        """
        Constructor of QuadTree
        :param bounds:
        :param max_objects:
        :param max_level:
        :param level:
        """
        self.__max_objects = max_objects
        self.__max_levels = max_level
        self.__level = level
        self.__bounds = bounds
        self.__nodes = []
        self.__objects = []

    def __repr__(self):
        return "<QuadTree: ({0}, {1}), {2}x{3}>".format(
            self.__bounds.x, self.__bounds.y, self.__bounds.width, self.__bounds.height
        )

    def __iter__(self):
        for obj in self.__objects:
            yield obj
        if not self.__is_leaf():
            for i in range(len(self.__nodes)):
                yield from self.__nodes[i]

    def __is_leaf(self):
        return not self.__nodes

    @property
    def node_num(self):
        return self.__total_nodes()

    def __total_nodes(self) -> int:
        total = 0
        if self.__nodes:
            for i in range(len(self.__nodes)):
                total += 1
                total += self.__nodes[i].__total_nodes()
        return total

    def clear(self):
        '''
        clear the quadtree
        :return:
        '''
        self.__objects = []
        if self.__nodes:
            for i in range(len(self.__nodes)):
                self.__nodes[i].clear()
        self.__nodes = []

    def split(self):
        '''
        split the quadtree into 4 subnodes
               root
               /||\
             / | | \
           NE NW SW SE
        :return:
        '''
        sub_width = self.__bounds.width / 2
        sub_height = self.__bounds.height / 2
        x = self.__bounds.x
        y = self.__bounds.y
        next_level = self.__level + 1

        self.__nodes.append(QuadTree(
            Bounds(x + sub_width, y, sub_width, sub_height),
            self.__max_objects,
            self.__max_levels,
            next_level)
        )

        self.__nodes.append(QuadTree(
            Bounds(x, y, sub_width, sub_height),
            self.__max_objects,
            self.__max_levels,
            next_level)
        )

        self.__nodes.append(QuadTree(
            Bounds(x, y + sub_height, sub_width, sub_height),
            self.__max_objects,
            self.__max_levels,
            next_level)
        )

        self.__nodes.append(QuadTree(
            Bounds(x + sub_width, y + sub_height, sub_width, sub_height),
            self.__max_objects,
            self.__max_levels,
            next_level)
        )

    # 0-3 denote 4 directions - north-east, north-west, south-west, south-east/ NE, NW, SW, SE
    def get_index(self, bounds: Union[Bounds, Point]):
        '''
        determine which node the object belongs to
        +-------+------+
        ｜ NW,1 | NE,0 |
        +-------+------+
        |  SW,2 | SE,4 |
        +-------+------+
        :param bounds:
        :return:
        '''
        index = -1
        vertical_midpoint = self.__bounds.x + (self.__bounds.width / 2)
        horizontal_midpoint = self.__bounds.y + (self.__bounds.height / 2)
        is_north = bounds.y < horizontal_midpoint
        is_south = bounds.y > horizontal_midpoint
        is_west = bounds.x < vertical_midpoint
        is_east = bounds.x > vertical_midpoint

        if is_east and is_north:
            index = 0
        elif is_west and is_north:
            index = 1
        elif is_west and is_south:
            index = 2
        elif is_east and is_south:
            index = 3
        return index

    def insert(self, bounds: Union[Bounds, Point]):
        """
        insert elements into quadtree
        :param bounds
        :return:
        """
        # Check if this node has subnodes
        # If True, insert it into matching subnodes
        if self.__nodes:
            index = self.get_index(bounds)
            if index != -1:
                self.__nodes[index].insert(bounds)
                return
        # if False, store objects here
        self.__objects.append(bounds)
        # if
        if len(self.__objects) > self.__max_objects and self.__level < self.__max_levels:
            if not self.__nodes:
                self.split()
            for i in range(len(self.__objects)):
                index = self.get_index(self.__objects[i])
                if index != -1:
                    self.__nodes[index].insert(self.__objects[i])
            self.__objects.clear()

    def retrieve(self, bounds: Union[Bounds, Point]) -> List[Union[Bounds]]:
        """
        get all objects in all nodes that may collide with given object
        :param bounds:
        :return: List[Bounds]
        """
        index = self.get_index(bounds)
        return_objects = self.__objects

        if self.__nodes:
            if index != -1:
                return_objects.append(self.__nodes[index].retrieve(bounds))
            else:
                for i in range(len(self.__nodes)):
                    return_objects.append(self.__nodes[i].retrieve(bounds))
        return return_objects

    def retrieve_intersections(self, bounds: Union[Bounds, Point]) -> List[Union[Bounds, Point]]:
        """
        get all objects in all nodes that intersect with given object
        :param bounds:
        :return: List[Bounds]:
        """
        found_bounds = []
        potentials: List[Union[Bounds, Point]] = self.retrieve(bounds)
        for i in range(len(potentials)):
            if bounds.intersects(potentials[i]):
                found_bounds.append(potentials[i])
        return found_bounds

    def find(self, bounds: Union[Bounds, Point]) -> List[int]:
        """
        find the indices of a given bounds
        :param bounds:
        :return: List[int]
        """
        index = self.get_index(bounds)
        if index != -1:
            self.__indices.append(index)
        if self.__nodes:
            index = self.get_index(bounds)
            if index != -1:
                self.__nodes[index].find(bounds)
        return self.__indices

    def contains_point(self, point: Point) -> bool:
        """
        check whether the provided point is in the node
        :param point:
        :return bool:
        """
        if self.__is_leaf():
            if self.__bounds.x <= point.x <= self.__bounds.x + self.__bounds.width and self.__bounds.y <= point.y <= self.__bounds.y + self.__bounds.height:
                return True
        return False

    def neighbors(self, point: Point, radius: float, max_num: int = 10) -> List:
        """
        find out neighboring points
        :param point:
        :param radius:
        :param max_num:
        :return List:
        """
        pass

    def visualize(self, size=15):
        """
        visualize all the objects and nodes
        :param size:
        :return:
        """
        from matplotlib import pyplot as plt
        from matplotlib import patches

        fig, ax = plt.subplots(1, 1, figsize=(size, size))

        def draw_all_nodes(node):
            if node.__is_leaf():
                for point in node.__objects:
                    plt.plot(point.x, point.y, '.')
            else:
                draw_rect(node)
                for i in range(len(node.__nodes)):
                    draw_rect(node.__nodes[i])
                    draw_all_nodes(node.__nodes[i])

        def draw_rect(node):
            ax.add_patch(patches.Rectangle((node.__bounds.x, node.__bounds.y), node.__bounds.width, node.__bounds.height, edgecolor='grey', linewidth=0.5, fill=False))

        plt.axis([self.__bounds.x,
                  self.__bounds.x + self.__bounds.width,
                  self.__bounds.y,
                  self.__bounds.y + self.__bounds.height])
        draw_all_nodes(self)
        # plt.savefig(os.path.abspath(os.curdir) + '/imgs/quadtree_demo_1.jpg')
        plt.show()

