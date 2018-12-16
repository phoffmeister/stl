import struct
import math


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


class Stl():
    def __init__(self):
        self.data = []

    def write_stl(self, file_path):
        print(f'Writing {len(self.data)} facets.')
        with open(file_path, 'w') as f:
            f.write('solid rock\n')
            for tri in self.data:
                f.write(f'facet normal {tri.n.x:E} {tri.n.x:E} {tri.n.z:E}\n')
                f.write('  outer loop\n')
                f.write(f'    vertex {tri.a.x:E} {tri.a.y:E} {tri.a.z:E}\n')
                f.write(f'    vertex {tri.b.x:E} {tri.b.y:E} {tri.b.z:E}\n')
                f.write(f'    vertex {tri.c.x:E} {tri.c.y:E} {tri.c.z:E}\n')
                f.write('  endloop\n')
                f.write('endfacet\n')
            f.write('endsolid rock')

    def write_stl_bin(self, file_path):
        with open(file_path, 'wb') as f:
            # write header -> 80 bytes
            f.write(b'a'*80)
            # write number of triangles -> uint32 -> (4byte)
            f.write(struct.pack('<i', len(self.data)))
            # write triangles n -> a -> b -> c -> 2byte 0
            for tri in self.data:
                f.write(struct.pack('<3f', tri.n.x, tri.n.y, tri.n.z))
                f.write(struct.pack('<3f', tri.a.x, tri.a.y, tri.a.z))
                f.write(struct.pack('<3f', tri.b.x, tri.b.y, tri.b.z))
                f.write(struct.pack('<3f', tri.c.x, tri.c.y, tri.c.z))
                f.write(struct.pack('\x00'*2))


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
    def __init__(self, r, facets, rings):
        super().__init__()
        # upper half
        top = Vector3(0, 0, r)
        bottom = Vector3(0, 0, -r)
        m_ring = Vector3.get_circle(r, 0, facets, 0)
        old_ring = m_ring
        new_ring = None
        # h = [r*0.2]
        # for n in range(1, rings):
        #     h.append(h[0] - 0.2 * h[n - 1] + h[n - 1])
        h = []
        h_sum = 0
        for i in range(rings - 1):
            h_sum += float(r/rings)
            h.append(h_sum)

        for n in range(rings - 1):
            new_r = math.sqrt(r**2 - h[n]**2)
            new_ring = Vector3.get_circle(
                    new_r,
                    h[n],
                    facets,
                    (n + 1) * 180 / facets)
            for p in range(facets - 1):
                self.data.append(Triangle(
                    old_ring[p],
                    old_ring[p + 1],
                    new_ring[p]))
                self.data.append(Triangle(
                    old_ring[p + 1],
                    new_ring[p],
                    new_ring[p + 1]))
            self.data.append(Triangle(
                old_ring[-1],
                old_ring[0],
                new_ring[-1]))
            self.data.append(Triangle(
                old_ring[0],
                new_ring[-1],
                new_ring[0]))
            old_ring = new_ring
        # stitch it to the top
        for p in range(facets):
            self.data.append(Triangle(
                top,
                new_ring[p-1],
                new_ring[p]))

        old_ring = m_ring
        for n in range(rings - 1):
            new_r = math.sqrt(r**2 - h[n]**2)
            new_ring = Vector3.get_circle(
                    new_r,
                    -h[n],
                    facets,
                    (n + 1) * 180 / facets)
            for p in range(facets - 1):
                self.data.append(Triangle(
                    old_ring[p],
                    old_ring[p + 1],
                    new_ring[p]))
                self.data.append(Triangle(
                    old_ring[p + 1],
                    new_ring[p],
                    new_ring[p + 1]))
            self.data.append(Triangle(
                old_ring[-1],
                old_ring[0],
                new_ring[-1]))
            self.data.append(Triangle(
                old_ring[0],
                new_ring[-1],
                new_ring[0]))
            old_ring = new_ring
        # stitch it to the bottom
        for p in range(facets):
            self.data.append(Triangle(
                bottom,
                new_ring[p-1],
                new_ring[p]))


if __name__ == '__main__':
    msphere = Sphere(10, 20, 20)
    msphere.write_stl("sphere.stl")
    mcyl = Cylinder(10, 20, 90)
    mcyl.write_stl("cylinder.stl")
    Sphere(10, 160, 80).write_stl("g_sphere.stl")
