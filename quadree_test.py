from quadtree import QuadTree, Bounds, Point
import random

if __name__ == '__main__':
    # turtle.hideturtle()
    # turtle.screensize(250, 250)
    my_tree = QuadTree(Bounds(0, 0, 400, 400), max_objects=4, max_level=5)
    for i in range(1000):
        x = random.random() * 400
        y = random.random() * 400
        # draw_point(x, y, 'red', 7)
        point = Point(x, y)
        my_tree.insert(point)
    my_tree.insert(Point(15, 325))
    my_tree.visualize()
    # draw_point(15, 325, 'blue', 12)
    # turtle.up()
    # turtle.goto(-185, 50)
    # turtle.down()
    # turtle.circle(100)
    # my_tree.plot()
    # print(len(my_tree.neighbors(Bounds(15, 235), radius=10)))
    # print(my_tree.node_num)
    # print(my_tree.find(Bounds(15, 325)))
    # turtle.mainloop()
