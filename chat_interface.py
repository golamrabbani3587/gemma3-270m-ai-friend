# girlfriend_chat_app.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import gradio as gr

# Load the improved fine-tuned model
base_model_id = "google/gemma-3-270m-it"
adapter_path = "./trained_model"

print(f"Loading base model: {base_model_id}")
print(f"Loading trained adapter from: {adapter_path}")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model_id)
tokenizer.pad_token = tokenizer.eos_token

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    device_map="auto",
    torch_dtype=torch.float32,
    token=True
)

# Load the improved fine-tuned adapter
model = PeftModel.from_pretrained(model, adapter_path)
model.eval()

def chat_with_girlfriend(message, history):
    """Chat function that uses the fine-tuned conversational model"""
    try:
        # Build conversation context
        conversation = ""
        
        # Add conversation history
        if history:
            for user_msg, bot_msg in history:
                conversation += f"<start_of_turn>user\n{user_msg}<end_of_turn>\n"
                conversation += f"<start_of_turn>model\n{bot_msg}<end_of_turn>\n"
        
        # Add current message
        conversation += f"<start_of_turn>user\n{message}<end_of_turn>\n<start_of_turn>model\n"
        
        # Tokenize
        inputs = tokenizer(conversation, return_tensors="pt", truncation=True, max_length=1024)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.8,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.eos_token_id,
            )
        
        # Decode response
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the model's response
        response = full_response.split("<start_of_turn>model\n")[-1].split("<end_of_turn>")[0].strip()
        
        # Clean up any remaining special tokens
        response = response.replace("<start_of_turn>", "").replace("<end_of_turn>", "").strip()
        
        return response
        
    except Exception as e:
        print(f"Error: {e}")
        return "I'm here for you, baby! 💕 What's on your mind?"

# Create interface with girlfriend theme
demo = gr.ChatInterface(
    fn=chat_with_girlfriend,
    title="💬 AI Chat Companion",
    description="A fine-tuned conversational AI model for emotional support and companionship! 💕",
    examples=[
        "Hey baby, how was your day?",
        "I'm feeling really stressed...",
        "I miss you so much",
        "I love you",
        "I need a hug",
        "I'm so happy today!",
        "Goodnight, sweetheart",
        "I'm feeling sad",
        "What do you love about us?",
        "I'm nervous about tomorrow"
    ],
    theme=gr.themes.Soft(
        primary_hue="pink",
        secondary_hue="pink",
        neutral_hue="pink"
    )
)

if __name__ == "__main__":
    print("Starting AI chat companion... 💬")
    demo.launch(share=True)
