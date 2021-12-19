import argparse


parser = argparse.ArgumentParser()

parser.add_argument(
    "-t", "--token",
    required=True,
    help="Your Discord API token",
    dest="token",
    metavar="<value>"
)

arguments = parser.parse_args()
