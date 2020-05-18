import sys
from tweet_metrics.metrics import parse_metrics


def __main__():
    metrics = parse_metrics(str(sys.argv[1]))
    return metrics


if __name__ == '__main__':
    __main__()
