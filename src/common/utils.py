import config
import argparse


def parse_terminal_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process weather data and generate Excel report"
    )
    parser.add_argument(
        "--make_report", action="store_true", help="Generate Excel report"
    )
    return parser.parse_args()


def get_pause_time() -> float:
    requests_per_hour = config.REQUESTS_PER_HOUR
    return 60 / requests_per_hour * 60


print(parse_terminal_args())
