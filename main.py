import argparse

from dpop import dcop_process


def main():
    parser = argparse.ArgumentParser(description='dcop')
    parser.set_defaults(func=dcop_process)
    parser.add_argument("agents_number", type=str, help="agents number")

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)


if __name__ == '__main__':
    main()
