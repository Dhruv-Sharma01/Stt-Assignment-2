"""
Repository Mining and Bug-Fixing Commit Extraction
CS202 Software Tools and Techniques for CSE
Lab Topic: Commit Message Rectification for Bug-Fixing Commits in the Wild
"""

import csv
from pydriller import Repository

# CONFIGURATION
REPO_URL = "repo_clone"  # Use local cloned repo for mining
BUG_KEYWORDS = ["fix", "bug", "error", "issue", "patch"]
OUTPUT_CSV = "bug_fixing_commits.csv"


def is_bug_fixing_commit(message):
    """Return True if commit message contains bug-fixing keywords."""
    message = message.lower()
    return any(kw in message for kw in BUG_KEYWORDS)


def mine_repository(repo_url, output_csv):
    with open(output_csv, "w", newline="") as csvfile:
        fieldnames = [
            "hash", "message", "parent_hashes", "is_merge_commit", "modified_files"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Specify main branch for mining
        for commit in Repository(repo_url, only_in_branch="main").traverse_commits():
            if is_bug_fixing_commit(commit.msg):
                writer.writerow({
                    "hash": commit.hash,
                    "message": commit.msg,
                    "parent_hashes": ",".join(commit.parents),
                    "is_merge_commit": commit.merge,
                    "modified_files": ",".join([mod.filename for mod in commit.modified_files])
                })

if __name__ == "__main__":
    mine_repository(REPO_URL, OUTPUT_CSV)
    print(f"Bug-fixing commits extracted to {OUTPUT_CSV}")
