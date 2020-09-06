# quadtree-py
![](https://img.shields.io/badge/license-MIT-success?style=for-the-badge&logo=appveyor) ![](https://img.shields.io/badge/quadtreepy-1.0.0-blue?style=for-the-badge&logo=appveyor) 
![](https://img.shields.io/badge/test-passing-red?style=for-the-badge&logo=appveyor)
> Quadtree is an essential data structure in the realm of GIS (Geographic Information System) which is able to build spatial
> index, perform spatial analysis, and compress data.

The visualization of quadtree is displayed as following:
![](https://github.com/Vezarachan/quadtree-py/blob/master/imgs/quadtree_demo_1.jpg)
## Usage
```python
from quadtree import QuadTree, Bounds, Point
import json

if __name__ == '__main__':
    my_tree = QuadTree(Bounds(0, 0, 400, 400), max_objects=4, max_level=5)
    # get point data from json file
    with open('path/to/json/example_data.json', 'r') as f:
        json_data = json.loads(f.read())
        point_set = json_data['data']
    # insert points
    for point in point_set:
        my_tree.insert(Point(point['x'], point['y'], point['value']))   
    # visualize quadtree
    my_tree.visualize()
```
## TODO
- [ ] nearest neighbors
- [ ] spatial analysis
