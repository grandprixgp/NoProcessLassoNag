import os, sys, mmap, re

target = 'ProcessLasso.exe'

patches = (
    {'name': 'first jnz instruction', 'original': b'\x75', 'patch': b'\x74', 'signature': b'\xE8....\x41\x3A\xC5\x75\x2E\x84\xDB\x75\x2A', 'offset': 8},
    {'name': 'second jnz instruction', 'original': b'\x75', 'patch': b'\x74', 'signature': b'\xE8....\x41\x3A\xC5\x74\x2E\x84\xDB\x75\x2A', 'offset': 12},
)

def scan(file, patch):
    result = re.search(patch['signature'], file.read())
    if result is not None:
        position = result.start() + patch['offset']
        file.seek(position)
        if (file.read(len(patch['original'])) == patch['original']):
            return result.start() + patch['offset']
    return None

def main():
    inline = True if (len(sys.argv) > 1 and sys.argv[1] == "inline") else False
    if inline:
        os.rename(target, target[:target.find('.')] + '_original' + target[target.find('.'):])
    with open('ProcessLasso_original.exe' if inline else 'ProcessLasso.exe', 'r+b' ) as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_COPY)
        for patch in patches:
            print(f"Searching for: {patch['name']}")
            mm.seek(0)
            patch_location = scan(mm, patch)
            if patch_location:
                mm.seek(patch_location)
                mm.write(patch['patch'])
                print(f"{hex(patch_location)}: 0x{patch['original'].hex()} -> 0x{patch['patch'].hex()}")
            else:
                print(f"Unable to find: {patch['name']}")
        if input("Write patch to disk? y/n ") == "y":
            with open('ProcessLasso.exe' if inline else 'ProcessLasso_patched.exe', 'w+b') as p:
                mm.seek(0)
                for byte in mm:
                    p.write(byte)
        else:
            if inline:
                f.close()
                mm.close()
                os.rename(target[:target.find('.')] + '_original' + target[target.find('.'):], target)

if __name__ == '__main__':
    main()