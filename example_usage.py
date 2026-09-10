from client import BowyerWatsonDelaunay

def main():
    print("=== Testing Bowyer-Watson Delaunay Triangulation ===")
    bw = BowyerWatsonDelaunay()
    pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0)]

    triangles = bw.triangulate(pts)
    print(f"Computed {len(triangles)} Delaunay triangles:")
    for t in triangles:
        print(" ", t)

    assert len(triangles) >= 2
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
