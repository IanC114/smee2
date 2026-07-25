import argparse

def get_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="increase logging verbosity; can be used multiple times"
    )

    return parser.parse_args()
