from transformers import CLIPTokenizer

# Initialize the tokenizer
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")

# The provided prompt
prompt = ""
# Tokenize the prompt
tokens = tokenizer(prompt)["input_ids"]

# Get the token count
print(len(tokens))
