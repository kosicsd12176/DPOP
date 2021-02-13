import argparse
import time

from dpop import dcop_process


def main():
    start = time.perf_counter()
    parser = argparse.ArgumentParser(description='dcop')
    parser.set_defaults(func=dcop_process)
    parser.add_argument("agents_number", type=str, help="agents number")

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    finish = time.perf_counter()
    print("finished in {}".format(finish - start))


if __name__ == '__main__':
    main()
