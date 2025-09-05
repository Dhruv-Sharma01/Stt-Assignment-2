"""
Diff Extraction and Analysis for Bug-Fixing Commits
CS202 Software Tools and Techniques for CSE
"""

import csv
from pydriller import Repository

REPO_URL = "https://github.com/pallets/flask"  # Use the same repo as before
LOCAL_REPO_PATH = "repo_clone"
COMMITS_CSV = "bug_fixing_commits.csv"
OUTPUT_CSV = "bug_fixing_diffs.csv"


def load_commit_hashes(csv_path):
    hashes = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hashes.append(row["hash"])
    return hashes


import os
import shutil
from git import Repo, InvalidGitRepositoryError

def clone_repo(repo_url, local_path):
    # If folder exists, check if it's a valid git repo
    if os.path.exists(local_path):
        try:
            _ = Repo(local_path)
            print(f"Repository already cloned at {local_path}.")
            return
        except InvalidGitRepositoryError:
            print(f"Invalid git repository at {local_path}, deleting...")
            shutil.rmtree(local_path)
    print(f"Cloning {repo_url} to {local_path}...")
    Repo.clone_from(repo_url, local_path)

def extract_diffs(local_repo_path, commit_hashes, output_csv):
    from git import Repo
    repo = Repo(local_repo_path)
    with open(output_csv, "w", newline="") as csvfile:
        fieldnames = [
            "hash", "message", "filename", "source_code_before", "source_code_current", "diff", "llm_inference", "rectified_message"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for h in commit_hashes:
            try:
                repo.commit(h)
            except Exception:
                print(f"Skipping missing commit: {h}")
                continue
            try:
                for commit in Repository(local_repo_path, only_commits=[h]).traverse_commits():
                    for mod in commit.modified_files:
                        writer.writerow({
                            "hash": commit.hash,
                            "message": commit.msg,
                            "filename": mod.filename,
                            "source_code_before": mod.source_code_before if mod.source_code_before else "",
                            "source_code_current": mod.source_code if mod.source_code else "",
                            "diff": mod.diff,
                            "llm_inference": "",  # Placeholder
                            "rectified_message": ""  # Placeholder
                        })
            except Exception as e:
                print(f"Error processing commit {h}: {e}")

if __name__ == "__main__":
    hashes = load_commit_hashes(COMMITS_CSV)
    clone_repo(REPO_URL, LOCAL_REPO_PATH)
    extract_diffs(LOCAL_REPO_PATH, hashes, OUTPUT_CSV)
    print(f"Diffs extracted to {OUTPUT_CSV}")
