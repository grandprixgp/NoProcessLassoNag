import os, sys, mmap, re

target = 'ProcessLasso.exe'

patches = (
	{'name': 'cmp patch', 'original': b'\x01', 'patch': b'\x00', 'signature': b'\x0F\xB6\xDB\x66\x85\xC0\xB8\x01\x00\x00\x00\x0F\x44\xD8\xE8(.|\s)(.|\s)(.|\s)(.|\s)\x3C\x01', 'offset': 21},
)

def scan(file, patch):
	results = re.finditer(patch['signature'], file.read())
	if results is not None:		
		for result in results:
			print(result)
			position = (result.start() + patch['offset']) - 1
			file.seek(position)
			if (file.read(len(patch['original'])) == patch['original']):
				return position
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