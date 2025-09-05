"""
Evaluation Script for Commit Message Rectification
Aggregates results for RQ1, RQ2, RQ3 and prints summary statistics.
"""
import csv

INPUT_CSV = "bug_fixing_diffs_rectified.csv"

rq1_similarities = []
rq2_lengths = []
rq3_keywords = 0
total = 0
rectification_types = {}

with open(INPUT_CSV, "r") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        total += 1
        rq1_similarities.append(float(row.get("rq1_similarity", 0)))
        rq2_lengths.append(int(row.get("rq2_length", 0)))
        if row.get("rq3_keyword", "False") in ["True", "true", "1"]:
            rq3_keywords += 1
        rect_type = row.get("rectification_type", "unknown")
        rectification_types[rect_type] = rectification_types.get(rect_type, 0) + 1

print("Evaluation Results:")
print(f"Total samples: {total}")
if total:
    print(f"RQ1: Average similarity: {sum(rq1_similarities)/total:.3f}")
    print(f"RQ2: Average length difference: {sum(rq2_lengths)/total:.2f}")
    print(f"RQ3: Bug keyword present in {rq3_keywords}/{total} ({rq3_keywords/total*100:.1f}%) messages")
    print("Rectification type counts:")
    for k, v in rectification_types.items():
        print(f"  {k}: {v}")
else:
    print("No data to evaluate.")
