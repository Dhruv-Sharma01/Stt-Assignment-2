"""
Plots for Assignment Evaluation (RQ1, RQ2, RQ3)
Generates and saves plots for similarity, length difference, bug keyword presence, and rectification type counts.
"""
import csv
import matplotlib.pyplot as plt

INPUT_CSV = "bug_fixing_diffs_rectified.csv"

rq1_similarities = []
rq2_lengths = []
rq3_keywords = []
rectification_types = {}

with open(INPUT_CSV, "r") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        rq1_similarities.append(float(row.get("rq1_similarity", 0)))
        rq2_lengths.append(int(row.get("rq2_length", 0)))
        rq3_keywords.append(row.get("rq3_keyword", "False") in ["True", "true", "1"])
        rect_type = row.get("rectification_type", "unknown")
        rectification_types[rect_type] = rectification_types.get(rect_type, 0) + 1

# RQ1: Similarity distribution
plt.figure(figsize=(8,4))
plt.hist(rq1_similarities, bins=50, color='skyblue', edgecolor='black')
plt.title('RQ1: Similarity Distribution')
plt.xlabel('Similarity')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('rq1_similarity_distribution.png')
plt.close()

# RQ2: Length difference distribution
plt.figure(figsize=(8,4))
plt.hist(rq2_lengths, bins=50, color='salmon', edgecolor='black')
plt.title('RQ2: Length Difference Distribution')
plt.xlabel('Length Difference (rectified - original)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('rq2_length_difference_distribution.png')
plt.close()

# RQ3: Bug keyword presence
plt.figure(figsize=(5,5))
labels = ['Contains Bug Keyword', 'Does Not Contain']
counts = [sum(rq3_keywords), len(rq3_keywords)-sum(rq3_keywords)]
plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=['lightgreen','lightgray'])
plt.title('RQ3: Bug Keyword Presence')
plt.tight_layout()
plt.savefig('rq3_bug_keyword_presence.png')
plt.close()

# Rectification type counts
plt.figure(figsize=(6,4))
types = list(rectification_types.keys())
counts = [rectification_types[t] for t in types]
plt.bar(types, counts, color='mediumpurple', edgecolor='black')
plt.title('Rectification Type Counts')
plt.xlabel('Type')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('rectification_type_counts.png')
plt.close()

print("All plots generated and saved as PNG files.")
