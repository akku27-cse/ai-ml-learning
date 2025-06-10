from transformers import pipeline

# Load model pipeline once on startup
# Use a smaller model for faster response, e.g., distilgpt2 or gpt2-medium
generator = pipeline("text-generation", model="distilgpt2", max_length=100)

def generate_response(prompt: str) -> str:
    # You can prepend some system prompt or context here if needed
    generated = generator(prompt, max_length=100, num_return_sequences=1)
    text = generated[0]["generated_text"]

    # Remove original prompt from response, keep only the generated continuation
    if text.startswith(prompt):
        text = text[len(prompt):].strip()

    return text
