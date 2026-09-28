from client import DelaunayTriangulation

points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (0.5, 0.5)]
triangles = DelaunayTriangulation.triangulate(points)

print(f"Computed {len(triangles)} Delaunay triangles:")
for i, tri in enumerate(triangles):
    print(f"  Triangle {i+1}: {tri}")
