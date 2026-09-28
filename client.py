"""Bowyer-Watson Incremental Delaunay Triangulation Engine.
100% Python Standard Library.
"""

import math

class DelaunayTriangulation:
    """Bowyer-Watson incremental 2D Delaunay triangulation."""
    @staticmethod
    def circumcircle(p1, p2, p3):
        """Returns ((center_x, center_y), radius) of triangle circumcircle."""
        d = 2 * (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))
        if abs(d) < 1e-12:
            return None, float("inf")
        ux = ((p1[0]**2 + p1[1]**2) * (p2[1] - p3[1]) +
              (p2[0]**2 + p2[1]**2) * (p3[1] - p1[1]) +
              (p3[0]**2 + p3[1]**2) * (p1[1] - p2[1])) / d
        uy = ((p1[0]**2 + p1[1]**2) * (p3[0] - p2[0]) +
              (p2[0]**2 + p2[1]**2) * (p1[0] - p3[0]) +
              (p3[0]**2 + p3[1]**2) * (p2[0] - p1[0])) / d
        r = math.hypot(p1[0] - ux, p1[1] - uy)
        return (ux, uy), r

    @classmethod
    def triangulate(cls, points):
        pts = list(set(points))
        if len(pts) < 3:
            return []

        min_x = min(p[0] for p in pts)
        max_x = max(p[0] for p in pts)
        min_y = min(p[1] for p in pts)
        max_y = max(p[1] for p in pts)

        dx = (max_x - min_x) * 10
        dy = (max_y - min_y) * 10
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2

        p_super1 = (mid_x - dx, mid_y - dy)
        p_super2 = (mid_x, mid_y + dy)
        p_super3 = (mid_x + dx, mid_y - dy)
        super_pts = {p_super1, p_super2, p_super3}

        triangles = [(p_super1, p_super2, p_super3)]

        for p in pts:
            bad_triangles = []
            for tri in triangles:
                center, radius = cls.circumcircle(tri[0], tri[1], tri[2])
                if center is not None and math.hypot(p[0] - center[0], p[1] - center[1]) <= radius + 1e-9:
                    bad_triangles.append(tri)

            edge_count = {}
            for tri in bad_triangles:
                edges = [
                    tuple(sorted((tri[0], tri[1]))),
                    tuple(sorted((tri[1], tri[2]))),
                    tuple(sorted((tri[2], tri[0])))
                ]
                for e in edges:
                    edge_count[e] = edge_count.get(e, 0) + 1

            polygon_edges = [e for e, count in edge_count.items() if count == 1]
            triangles = [tri for tri in triangles if tri not in bad_triangles]

            for e in polygon_edges:
                triangles.append((e[0], e[1], p))

        final_triangles = [tri for tri in triangles if not any(v in super_pts for v in tri)]
        return final_triangles
