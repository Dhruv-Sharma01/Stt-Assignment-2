"""
LLM Inference for Commit Messages using CommitPredictorT5
Uses both diff and source code as input.
"""
import csv
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "mamiksik/CommitPredictorT5"
INPUT_CSV = "bug_fixing_diffs.csv"
OUTPUT_CSV = "bug_fixing_diffs_llm.csv"

# Load model and tokenizer
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def get_llm_inference(diff, src_before, src_after):
    # Combine diff and source code for input
    input_text = f"diff: {diff}\nsource_before: {src_before}\nsource_after: {src_after}"
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=64)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

with open(INPUT_CSV, "r") as infile, open(OUTPUT_CSV, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    if "llm_inference" not in fieldnames:
        fieldnames.append("llm_inference")
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        diff = row.get("diff", "")
        src_before = row.get("source_code_before", "")
        src_after = row.get("source_code_current", "")
        try:
            llm_result = get_llm_inference(diff, src_before, src_after)
        except Exception as e:
            llm_result = f"ERROR: {e}"
        row["llm_inference"] = llm_result
        writer.writerow(row)
print(f"LLM inference complete. Results saved to {OUTPUT_CSV}")
