import struct
import math


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'{self.x}, {self.y}, {self.z}'

    def __repr__(self):
        return (self.x, self.y, self.z)

    def __eq__(self, other):
        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z

    def __add__(self, other):
        return Vector3(self.x + other.x,
                       self.y + other.y,
                       self.z + other.z)


class Triangle:
    def __init__(self, n, a, b, c):
        self.n = n
        self.a = a
        self.b = b
        self.c = c


class Stl():
    def __init__(self):
        self.data = []

    def write_stl(self, file_path):
        print(f'Writing {len(self.data)} facets.')
        with open(file_path, 'w') as f:
            # write header -> 80 bytes
            f.write('solid rock\n')
            # write triangles n -> a -> b -> c -> 2byte 0
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
        n = Vector3(0, 0, 0)
        c1 = self._get_circle(r, 0, facets)
        c1_center = Vector3(0, 0, 0)
        c2 = self._get_circle(r, h, facets)
        c2_center = Vector3(0, 0, h)

        for p in range(len(c1)-1):
            self.data.append(Triangle(n, c1[p], c1[p+1], c1_center))
        self.data.append(Triangle(n, c1[0], c1[-1], c1_center))

        for p in range(len(c2)-1):
            self.data.append(Triangle(n, c2[p], c2[p+1], c2_center))
        self.data.append(Triangle(n, c2[0], c2[-1], c2_center))

        for p in range(len(c1)-1):
            self.data.append(Triangle(n, c1[p], c1[p+1], c2[p]))
            self.data.append(Triangle(n, c1[p+1], c2[p], c2[p+1]))
        self.data.append(Triangle(n, c1[-1], c1[0], c2[-1]))
        self.data.append(Triangle(n, c1[0], c2[0], c2[-1]))

    def _get_circle(self, r, z, amount):
        circle = []
        deg = float(360.0 / amount)
        for n in range(amount):
            x = r * math.sin(math.radians(n * deg))
            y = r * math.cos(math.radians(n * deg))
            circle.append(Vector3(x, y, z))
        return circle


if __name__ == '__main__':
    mstl = Cylinder(10, 50, 300)
    mstl.write_stl("cyl2.stl")
