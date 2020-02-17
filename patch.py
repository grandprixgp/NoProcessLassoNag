import os, sys, mmap

target = 'ProcessLasso.exe'

patches = (
    {'offset': 0x56C31, 'original': b'\x75', 'patch': b'\x74'},
    {'offset': 0x56C35, 'original': b'\x75', 'patch': b'\x74'},
)

def main():
    inline = True if (len(sys.argv) > 1 and sys.argv[1] == "inline") else False
    if inline:
        os.rename(target, target[:target.find('.')] + '_original' + target[target.find('.'):])
    with open('ProcessLasso_original.exe' if inline else 'ProcessLasso.exe', 'r+b' ) as f:
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
            with open('ProcessLasso.exe' if inline else 'ProcessLasso_patched.exe', 'w+b') as p:
                for byte in mm:
                    p.write(byte)
        else:
            if inline:
                f.close()
                mm.close()
                os.rename(target[:target.find('.')] + '_original' + target[target.find('.'):], target)

if __name__ == '__main__':
    main()