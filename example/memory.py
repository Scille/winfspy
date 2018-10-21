import argparse
from winfspy import start_fs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("mountpoint")
    parser.add_argument("-d", dest='debug', action='store_true')
    args = parser.parse_args()
    start_fs(args.mountpoint, debug=args.debug)
