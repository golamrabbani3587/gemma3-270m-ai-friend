# test_improved_model.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

def test_improved_model():
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
    
    # Test prompts
    test_prompts = [
        "Hey baby, how was your day?",
        "I'm feeling really stressed about work...",
        "I miss you",
        "I love you",
        "I'm feeling sad",
        "I need a hug",
        "I'm so happy today!",
        "Goodnight, sweetheart"
    ]
    
    for prompt in test_prompts:
        print(f"\n{'='*60}")
        print(f"User: {prompt}")
        print(f"{'='*60}")
        
        # Build conversation
        conversation = f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"
        
        # Tokenize
        inputs = tokenizer(conversation, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=120,
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
        
        print(f"Model: {response}")
        print()

if __name__ == "__main__":
    test_improved_model()
