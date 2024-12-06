from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/blenderbot-400M-distill"

# Load model (download on first run and reference local installation for subsequent runs)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Initialize conversation history
conversation_history = []

print("Chat with Rana's bot! Type 'exit' to end the conversation.\n")

while True:
    # Display a prompt for user input
    user_input = input("You: ").strip()

    # Exit condition
    if user_input.lower() == "exit":
        print("Ending the conversation. Goodbye!")
        break

    # Add user input to conversation history
    conversation_history.append(f"User: {user_input}")

    # Prepare the model input
    history_string = "\n".join(conversation_history)
    inputs = tokenizer.encode(history_string, return_tensors="pt", truncation=True)

    # Generate a response
    outputs = model.generate(inputs, max_length=200, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Display the response
    print(f"Rana's bot: {response}")

    # Add model response to conversation history
    conversation_history.append(f"Rana's bot: {response}")
