from quadtree import QuadTree, Bounds, Point
import json
import matplotlib.pyplot as plt

if __name__ == '__main__':
    my_tree = QuadTree(Bounds(0, 0, 400, 400), max_objects=4, max_level=5)
    # get point data from json file
    with open('../tests/example_data.json', 'r') as f:
        json_data = json.loads(f.read())
        point_set = json_data['data']
    # insert points
    for point in point_set:
        my_tree.insert(Point(point['x'], point['y'], point['value']))
    # visualize quadtree
    objects = my_tree.retrieve(Bounds(200, 200, 50, 50))
    objects_intersects = my_tree.retrieve_intersections(Bounds(200, 200, 50, 50))
    nearest_neighbors = my_tree.nearest_neighbors(Point(225, 225), radius=25)
    print('collide ------------ ', len(objects))
    print('intersects --------- ', len(objects_intersects))
    print('nearest neighbors -- ', len(nearest_neighbors))
    my_tree.visualize()
