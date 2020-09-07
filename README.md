# <code>quadtree-py</code>
![](https://img.shields.io/badge/license-MIT-success?style=for-the-badge&logo=appveyor) ![](https://img.shields.io/badge/quadtreepy-1.0.0-blue?style=for-the-badge&logo=appveyor) 
![](https://img.shields.io/badge/test-passing-red?style=for-the-badge&logo=appveyor)
> Quadtree is an essential data structure in the realm of GIS (Geographic Information System) which is able to build spatial
> index, perform spatial analysis, and compress data.

The visualization of quadtree is displayed as following:
![](https://github.com/Vezarachan/quadtree-py/blob/master/docs/imgs/quadtree_demo_1.jpg)
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
    # retrieve objects that may collide with given boundingbox
    objects = my_tree.retrieve(Bounds(200, 200, 50, 50))
    # retrive objects that intersects with provided boundingbox
    objects_intersects = my_tree.retrieve_intersections(Bounds(200, 200, 50, 50))
    # retrieve nearest neighbors
    nearest_neighbors = my_tree.nearest_neighbors(Point(225, 225), radius=25, max_num=20)
```
## TODO
- [x] visualization
- [x] nearest neighbors
- [ ] spatial analysis
    - [ ] kernel density estimation (KDE)
    - [ ] spatial clustering
    
## Current Projects
- **quadtree-py** - A quadtree implementation in pure Python
- **cocopulas** - A Python lib for copulas (elliptical, archimedean copulas)

## Next Projects
- **KD-Tree** - The k-dimensional tree implementation in Python
- **V2ML** - Way to Machine Learning (Courses from Hung-yi Lee in NTU)
- **GeoBayesian** - Combination of Spatial Analysis and Bayesian Data Analysis
- **MicroGIS** - A lightweight, full-function, modern GIS based on C++
