import os
import csv
from transformers import pipeline

# ✅ This line creates the "output" folder automatically if it doesn't exist
os.makedirs("output", exist_ok=True)

corrector = pipeline("text2text-generation", model="./grammar_model")

transcripts = [
    "fix: hello my name is John and I will go to the market tomorrow",
    "fix: this is a reminder to finish your assignment by Friday",
]

# ✅ CSV will be saved inside output folder
csv_path = "output/corrected_texts.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Original", "Corrected"])

    for txt in transcripts:
        corrected = corrector(txt)[0]["generated_text"]
        writer.writerow([txt, corrected])
        print("Original:", txt)
        print("Corrected:", corrected)
        print("---")

print("✅ File saved successfully at:", csv_path)
