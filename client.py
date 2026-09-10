class BowyerWatsonDelaunay:
    """
    Bowyer-Watson Incremental Delaunay Triangulation.
    Tests circumcircle condition for 2D points.
    """
    def circumcircle_contains(self, tri, p):
        (x1, y1), (x2, y2), (x3, y3) = tri
        xp, yp = p
        d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        if abs(d) < 1e-9:
            return False
        ux = ((x1**2 + y1**2)*(y2 - y3) + (x2**2 + y2**2)*(y3 - y1) + (x3**2 + y3**2)*(y1 - y2)) / d
        uy = ((x1**2 + y1**2)*(x3 - x2) + (x2**2 + y2**2)*(x1 - x3) + (x3**2 + y3**2)*(x2 - x1)) / d
        r_sq = (x1 - ux)**2 + (y1 - uy)**2
        p_dist_sq = (xp - ux)**2 + (yp - uy)**2
        return p_dist_sq < r_sq

    def triangulate(self, points):
        super_tri = ((-100.0, -100.0), (100.0, -100.0), (0.0, 100.0))
        triangles = [super_tri]

        for p in points:
            bad_triangles = []
            for tri in triangles:
                if self.circumcircle_contains(tri, p):
                    bad_triangles.append(tri)

            polygon = []
            for tri in bad_triangles:
                edges = [
                    (tri[0], tri[1]),
                    (tri[1], tri[2]),
                    (tri[2], tri[0])
                ]
                for edge in edges:
                    shared = False
                    for other in bad_triangles:
                        if other == tri:
                            continue
                        other_edges = [
                            (other[0], other[1]), (other[1], other[0]),
                            (other[1], other[2]), (other[2], other[1]),
                            (other[2], other[0]), (other[0], other[2])
                        ]
                        if edge in other_edges:
                            shared = True
                            break
                    if not shared:
                        polygon.append(edge)

            triangles = [t for t in triangles if t not in bad_triangles]
            for edge in polygon:
                triangles.append((edge[0], edge[1], p))

        st_verts = set(super_tri)
        return [t for t in triangles if not (set(t) & st_verts)]
