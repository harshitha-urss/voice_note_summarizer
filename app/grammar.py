# grammar.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

print("⏳ Loading Grammar Correction Model (vennify/t5-base-grammar-correction)...")

tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction")

def correct_grammar(text: str) -> str:
    """
    Corrects grammar using a T5 model.
    Always returns corrected text (never crashes).
    """
    try:
        inp = "fix: " + text
        inputs = tokenizer(inp, return_tensors="pt")
        output = model.generate(**inputs, max_length=256)
        corrected = tokenizer.decode(output[0], skip_special_tokens=True)
        return corrected.strip()
    except Exception as e:
        print("Grammar correction error:", e)
        # fallback: simple autocorrect
        text = text.strip()
        if not text:
            return text
        text = text[0].upper() + text[1:]
        if text[-1] not in ".!?":
            text += "."
        return text
