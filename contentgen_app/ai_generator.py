from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='gpt2')
set_seed(42)

def generate_text(prompt, min_words=200):
    result = generator(prompt, max_new_tokens=300, num_return_sequences=1)
    text = result[0]['generated_text']
    words = text.split()

    while len(words) < min_words:
        more = generator(text, max_new_tokens=200, num_return_sequences=1, do_sample=True)[0]['generated_text']
        words += more.split()

    return ' '.join(words[:min_words])
  