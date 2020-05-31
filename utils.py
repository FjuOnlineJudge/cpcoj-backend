import os, sys, logging
import pprint

pp = pprint.PrettyPrinter(indent=4)
def dump(*args, **kwargs):
	pp.pprint(*args, **kwargs)

cur_path = lambda file: os.path.abspath(os.path.dirname(file))
proj_root = cur_path(__file__)

# .split()
# ' '.join()

log_path = os.path.join(proj_root, 'log')
file_name = 'oj'

class LoggerWriter:
    def __init__(self, level):
        self.level = level

    def write(self, message):
        if message != '\n':
            self.level(message)

    def flush(self):
        self.level(sys.stderr)

FORMAT = '%(asctime)15s - %(name)s - [%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt='%Y/%m/%d %I:%M:%S', handlers=[ \
		logging.FileHandler("{0}/{1}.log".format(log_path, file_name)) \
       ,logging.StreamHandler()])

# stderr = logging.getLogger('stderr')
# sys.stderr = LoggerWriter(stderr.warning)

def str_row(name, item, fmt='  {} = {}\n'):
	return fmt.format(name, item)