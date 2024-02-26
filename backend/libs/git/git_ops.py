# /backend/libs/git/git_ops.py
import subprocess
from ..misc.misc import get_formatted_timestamp


def run_git_command(command):
    """Runs a git command and returns its output"""
    try:
        output = subprocess.check_output(["git"] + command, stderr=subprocess.STDOUT)
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error running git command {' '.join(command)}:\n{e.output.decode()}")


def git_commit_and_push():
    """Commit and push all changes to Git."""
    timestamp = get_formatted_timestamp("%Y-%m-%d %H:%M:%S")
    commit_message = f"Update data and image: {timestamp}"
    
    # Run Git command to add all changes
    run_git_command(["add", "."])
    
    # Commit and push
    run_git_command(["commit", "-m", commit_message])
    run_git_command(["push"])