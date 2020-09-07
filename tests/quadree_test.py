from quadtree import QuadTree, Bounds, Point
import json
import unittest


class QuadTreeFunctionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.quadtree = QuadTree(Bounds(0, 0, 400, 400), max_objects=4, max_level=5)

    def test_points_insert(self):
        with open('./tests/example_data.json', 'r') as f:
            json_data = json.loads(f.read())
        points = json_data['data']
        for point in points:
            self.quadtree.insert(Point(point['x'], point['y'], point['value']))

    def test_retrieve(self):
        objects = self.quadtree.retrieve(Bounds(200, 200, 50, 50))

    def test_retrieve_intersections(self):
        objects = self.quadtree.retrieve_intersections(Bounds(200, 200, 50, 50))

    def test_nearest_neighbors(self):
        points = self.quadtree.nearest_neighbors(Point(225, 225), radius=25)

    def test_visualization(self):
        self.quadtree.visualize()

    def tearDown(self) -> None:
        self.quadtree.clear()


if __name__ == '__main__':
    unittest.main(verbosity=1)

