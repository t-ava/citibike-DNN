import argparse


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', metavar='I', type=str, default="127.0.0.1",
                        help='IP')
    parser.add_argument('--port', metavar='P', type=str, default="9650",
                        help='IP')

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parser()
    print(args)
