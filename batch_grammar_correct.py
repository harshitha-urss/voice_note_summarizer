from transformers import pipeline

corrector = pipeline("text2text-generation", model="./grammar_model")

transcripts = [
    "fix: hello my name is John and I will go to the market tomorrow",
]

for txt in transcripts:
    result = corrector(txt, max_length=128)[0]['generated_text']
    print("Original:", txt)
    print("Corrected:", result)
    print("---")
