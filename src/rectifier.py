"""
Rectifier for Commit Messages
Compares LLM-generated commit messages with original ones and applies simple rectification rules.
Outputs rectified messages and evaluation columns for RQ1, RQ2, RQ3.
"""
import csv
import difflib

INPUT_CSV = "bug_fixing_diffs_llm.csv"
OUTPUT_CSV = "bug_fixing_diffs_rectified.csv"

# Simple rectification: If LLM message is too short, fallback to original. If too similar, keep LLM.
def rectify_commit_message(original, llm):
    if not llm or len(llm.split()) < 3:
        return original, "fallback_short"
    # Similarity threshold (RQ1):
    similarity = difflib.SequenceMatcher(None, original, llm).ratio()
    if similarity > 0.8:
        return llm, "llm_similar"
    return llm, "llm_rectified"

with open(INPUT_CSV, "r") as infile, open(OUTPUT_CSV, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["rectified_message", "rectification_type", "rq1_similarity", "rq2_length", "rq3_keyword"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        original = row.get("commit_message", "")
        llm = row.get("llm_inference", "")
        rectified, rect_type = rectify_commit_message(original, llm)
        # RQ1: Similarity
        rq1_similarity = round(difflib.SequenceMatcher(None, original, rectified).ratio(), 3)
        # RQ2: Length difference
        rq2_length = len(rectified.split()) - len(original.split())
        # RQ3: Contains bug keyword
        bug_keywords = ["bug", "fix", "error", "issue"]
        rq3_keyword = any(kw in rectified.lower() for kw in bug_keywords)
        row.update({
            "rectified_message": rectified,
            "rectification_type": rect_type,
            "rq1_similarity": rq1_similarity,
            "rq2_length": rq2_length,
            "rq3_keyword": rq3_keyword
        })
        writer.writerow(row)
print(f"Rectification complete. Results saved to {OUTPUT_CSV}")
