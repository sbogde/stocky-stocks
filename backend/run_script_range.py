import subprocess
import sys
from datetime import datetime, timedelta

def parse_arguments():
    args = sys.argv[1:]
    args_dict = {}
    for arg in args:
        if arg.startswith("--"):
            key, value = arg.split("=")
            args_dict[key] = value
    return args_dict

def run_script_for_date_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    delta = timedelta(days=1)
    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        print(f"Running script for date: {date_str}")
        subprocess.run(["python", "./backend/script.py", f"--end-date={date_str}"])
        current += delta

if __name__ == "__main__":
    args = parse_arguments()
    start_date = args.get("--start-date")
    end_date = args.get("--end-date")
    if start_date and end_date:
        run_script_for_date_range(start_date, end_date)
    else:
        print("Please provide --start-date and --end-date parameters.")
