import sys, mmap

patches = (
    {'offset': 0x56C31, 'original': b'\x75', 'patch': b'\x74'},
    {'offset': 0x56C35, 'original': b'\x75', 'patch': b'\x74'},
)

def main():
    with open(sys.argv[1] if len(sys.argv) > 1 else 'ProcessLasso.exe', 'r+b') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_COPY)
        for patch in patches:
            mm.seek(patch['offset'])
            data = mm.read(len(patch['original']))
            if data == patch['original']:
                print("Patched 0x{0} at {1} to 0x{2}".format(data.hex(), hex(patch['offset']), patch['patch'].hex()))
                mm.seek(patch['offset'])
                mm.write(patch['patch'])
            else:
                print("Unable to locate patch at {0}".format(hex(patch['offset'])))
        if input("Write patch to disk? y/n ") == "y":
            with open('ProcessLasso_patched.exe', 'w+b') as p:
                for byte in mm:
                    p.write(byte)

if __name__ == '__main__':
    main()