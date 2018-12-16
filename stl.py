import struct


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
