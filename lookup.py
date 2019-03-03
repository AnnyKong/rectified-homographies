import peek,sys

def lookup():
	if len(sys.argv) != 2:
		print("  Please follow the format: python3 lookup.py <i>")
		exit(0)
	arg = sys.argv[1]
	i = int(arg)
	incomplete_imgs_sorted = peek.getAllImgPaths()
	return incomplete_imgs_sorted[i]

if __name__ == '__main__':
	file = lookup()
	print(file)