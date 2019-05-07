import os, sys
import pprint

pp = pprint.PrettyPrinter(indent=4)
def dump(*args, **kwargs):
	pp.pprint(*args, **kwargs)

cur_path = lambda file: os.path.abspath(os.path.dirname(file))
proj_root = cur_path(__file__)

# .split()
# ' '.join()


def str_row(name, item, fmt='  {} = {}\n'):
	return fmt.format(name, item)