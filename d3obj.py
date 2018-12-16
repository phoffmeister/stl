import math
from stl import Stl


class Vector3:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    @staticmethod
    def get_circle(r, z, amount, deg_offset=0):
        circle = []
        deg = float(360.0 / amount)
        for n in range(amount):
            x = r * math.sin(math.radians(n * deg + deg_offset))
            y = r * math.cos(math.radians(n * deg + deg_offset))
            circle.append(Vector3(x, y, z))
        return circle

    def unify(self):
        s = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        self.x /= s
        self.y /= s
        self.z /= s
        return self

    def __str__(self):
        return f'{self.x}, {self.y}, {self.z}'

    def __repr__(self):
        return f'{self.x}, {self.y}, {self.z}'

    def __eq__(self, other):
        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z

    def __add__(self, other):
        return Vector3(self.x + other.x,
                       self.y + other.y,
                       self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x,
                       self.y - other.y,
                       self.z - other.z)

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            return Vector3(self.x * other,
                           self.y * other,
                           self.z * other)
        else:
            return Vector3((self.y * other.z) - (self.z * other.y),
                           (self.z * other.x) - (self.x * other.z),
                           (self.x * other.y) - (self.y * other.x))

    def __truediv__(self, other):
        if type(other) is int or type(other) is float:
            return Vector3(self.x / float(other),
                           self.y / float(other),
                           self.z / float(other))
        else:
            raise TypeError('Cannot divide Vector by another')


class Triangle:
    def __init__(self, a, b, c):
        self.n = ((b - a) * (c - a)).unify()
        self.a = a
        self.b = b
        self.c = c


class Cylinder(Stl):
    def __init__(self, r, h, facets):
        super().__init__()
        c1 = Vector3.get_circle(r, 0, facets)
        c1_center = Vector3(0, 0, 0)
        c2 = Vector3.get_circle(r, h, facets)
        c2_center = Vector3(0, 0, h)

        for p in range(len(c1)-1):
            self.data.append(Triangle(c1[p], c1[p+1], c1_center))
        self.data.append(Triangle(c1[0], c1[-1], c1_center))

        for p in range(len(c2)-1):
            self.data.append(Triangle(c2[p], c2[p+1], c2_center))
        self.data.append(Triangle(c2[0], c2[-1], c2_center))

        for p in range(len(c1)-1):
            self.data.append(Triangle(c1[p], c1[p+1], c2[p]))
            self.data.append(Triangle(c1[p+1], c2[p], c2[p+1]))
        self.data.append(Triangle(c1[-1], c1[0], c2[-1]))
        self.data.append(Triangle(c1[0], c2[0], c2[-1]))


class Sphere(Stl):
    def __init__(self, r, facets, ring_n):
        super().__init__()

        rings = []
        deg_off = 0
        for n in range(ring_n):
            deg_off += 180 / (ring_n + 1)
            c_r = r * math.sin(math.radians(deg_off))
            c_h = r * math.cos(math.radians(deg_off))
            rings.append(Vector3.get_circle(
                c_r,
                c_h,
                facets,
                n * 180 / facets))

        # stitch top to first ring
        for p in range(facets):
            self.data.append(Triangle(
                Vector3(0, 0, r),
                rings[0][p-1],
                rings[0][p]))

        # stitch rings together
        for p in range(len(rings)-1):
            # ring p to ring p + 1
            for i in range(facets - 1):
                self.data.append(Triangle(
                    rings[p][i],
                    rings[p][i + 1],
                    rings[p + 1][i]))
                self.data.append(Triangle(
                    rings[p][i + 1],
                    rings[p + 1][i],
                    rings[p + 1][i + 1]))
            self.data.append(Triangle(
                rings[p][-1],
                rings[p][0],
                rings[p + 1][-1]))
            self.data.append(Triangle(
                rings[p][0],
                rings[p + 1][-1],
                rings[p + 1][0]))

        # stitch top to last ring
        for p in range(facets):
            self.data.append(Triangle(
                Vector3(0, 0, -r),
                rings[-1][p-1],
                rings[-1][p]))


if __name__ == '__main__':
    msphere = Sphere(10, 20, 19)
    msphere.write_stl("sphere.stl")
    mcyl = Cylinder(10, 20, 90)
    mcyl.write_stl("cylinder.stl")
    Sphere(10, 160, 80).write_stl("g_sphere.stl")
